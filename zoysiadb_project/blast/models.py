from django.db import models
from datetime import datetime
from django.conf import settings
from django.db import transaction

# Create your models here.
class BlastDBFILE(models.Model):
    #add_time = models.DateTimeField(default=datetime.now, verbose_name="Add_Time")
    db_type = [
        ('genome', 'Genome-wide Sequences'),
        ('mRNA', 'mRNA Sequences'),
        ('CDS', 'Coding Sequences'),
        ('protein', 'Protein Sequences')
        ]
    file_type = models.CharField(max_length=20, choices=db_type)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blast_db_files'

    @classmethod
    def update_from_media(cls):
        """扫描文件夹并更新数据库"""
        from pathlib import Path

        media_root = Path(settings.MEDIA_ROOT)
        blast_root = media_root / 'blast_db'
        file_type_ext_map = {
            'genome': '.genome',
            'mRNA': '.mrna',
            'CDS': '.cds',
            'protein': '.pep',
            }
        
        records = []
        for type_dir in blast_root.glob('*'):
            if type_dir.is_dir():
                file_type = type_dir.name
                main_ext = file_type_ext_map.get(file_type)

                for file_path in type_dir.rglob('*'):
                    if file_path.is_file():
                        rel_path = file_path.relative_to(media_root)
                        if main_ext and file_path.name.endswith(main_ext):
                            records.append(cls(
                                file_name = file_path.name,
                                file_type = file_type,
                                file_path = str(rel_path)
                                ))
                    
        with transaction.atomic():
            cls.objects.all().delete()
            cls.objects.bulk_create(records, batch_size=1000)