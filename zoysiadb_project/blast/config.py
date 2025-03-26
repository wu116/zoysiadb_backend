import os
from django.conf import settings
from .models import BlastDBFILE
from functools import lru_cache

@lru_cache()
def get_blast_config():
    config = {
        'blastn': {
            'databases': {}, 'command': 'blastn'
        },
        'blastp': {
            'databases': {}, 'command': 'blastp'
        },
        'blastx': {
            'databases': {}, 'command': 'blastx'
        },
        'tblastn': {
            'databases': {}, 'command': 'tblastn'
        },
        'tblastx': {
            'databases': {}, 'command': 'tblastx'
        },
    }

    db_type_to_program = {
        'CDS': ['blastn', 'blastx', 'tblastx'],
        'mRNA': ['blastn', 'blastx', 'tblastx'],
        'genome': ['blastn', 'blastx', 'tblastx'],
        'protein': ['blastp', 'tblastn'],
    }


    for entry in BlastDBFILE.objects.all():
        db_path = os.path.join(settings.MEDIA_ROOT, entry.file_path)
        db_key = entry.file_name
        program_list = db_type_to_program.get(entry.file_type, [])
        
        for program in program_list:
            config[program]['databases'][db_key] = str(db_path)
    
    return config