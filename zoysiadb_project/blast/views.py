from django.shortcuts import render
import json
import os
import uuid
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .config import BLAST_CONFIG

# Create your views here.

def blast_request(request):
    """处理 BLAST 请求的核心入口"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # 解析 JSON 数据
        data = json.loads(request.body)
        header = data.get('header', '')
        sequences = data.get('body', [])  # 假设前端传递数组
        program = data.get('program', 'blastn')
        db_key = data.get('db', 'CDS')
        evalue = data.get('evalue', '1e-25')

        # 验证参数有效性
        if program not in BLAST_CONFIG:
            raise ValueError(f"Invalid program: {program}")
        
        # 获取数据库路径
        db_path = BLAST_CONFIG[program]['databases'].get(db_key)
        if not db_path or not os.path.exists(db_path):
            raise ValueError(f"Database {db_key} not found")
        
        # 生成唯一文件名
        file_id = uuid.uuid4().hex
        input_path = os.path.join(settings.MEDIA_ROOT, f'blast_input_{file_id}.fasta')
        output_path = os.path.join(settings.MEDIA_ROOT, f'blast_output_{file_id}.txt')

        # 创建 FASTA 文件
        _create_fasta_file(input_path, header, sequences)
        
        # 执行 BLAST
        blast_results = _run_blast(input_path, output_path, program, db_path, evalue)
        
        # 清理临时文件
        _cleanup_files([input_path, output_path])

        return JsonResponse({
            'status': 'success',
            'results': blast_results
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        _cleanup_files([input_path, output_path])  # 异常时清理
        return JsonResponse({'error': str(e)}, status=500)
    
def _create_fasta_file(path, header, sequences):
    """生成 FASTA 格式文件"""
    with open(path, 'w') as f:
        f.write(f'>{header}\n')
        for seq in sequences:
            # 每行最多80字符（FASTA标准格式）
            formatted_seq = '\n'.join([seq[i:i+80] for i in range(0, len(seq), 80)])
            f.write(formatted_seq + '\n')

def _run_blast(input_path, output_path, program, db_path, evalue):
    """执行 BLAST 命令"""
    blast_cmd = [
        program,
        '-query', input_path,
        '-db', db_path,
        '-outfmt', '6',
        '-evalue', evalue,
        '-out', output_path
    ]

    result = subprocess.run(
        blast_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f'BLAST failed: {result.stderr}')
    
    # 解析结果文件
    return _parse_blast_output(output_path)

def _parse_blast_output(output_path):
    """解析 BLAST 输出文件"""
    results = []
    with open(output_path) as f:
        for line in f:
            # 解析 -outfmt 6 格式的字段
            fields = line.strip().split('\t')
            results.append({
                'qseqid': fields[0],
                'sseqid': fields[1],
                'pident': float(fields[2]),
                'evalue': float(fields[10]),
                'bitscore': float(fields[11])
            })
    return results

def _cleanup_files(paths):
    """清理临时文件"""
    for path in paths:
        if os.path.exists(path):
            os.remove(path)