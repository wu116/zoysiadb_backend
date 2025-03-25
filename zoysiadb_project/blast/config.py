import os
from django.conf import settings

BLAST_CONFIG = {
    'blastn': {
        'databases': {
            'ZJLY_hap1.cds': os.path.join(settings.MEDIA_ROOT, 'blast_db/CDS/ZJLY_hap1.cds'),
            'mouse': '/blast_db/mouse_genome.fa'
        },
        'command': 'blastn'
    },
    'blastp': {
        'databases': {
            'ZJLY_hap1.pep': os.path.join(settings.MEDIA_ROOT, 'blast_db/protein/ZJLY_hap1.pep')
        },
        'command': 'blastp'
    },
    'tblastn': {
        'databases': {
            'ZJLY_hap1.pep': os.path.join(settings.MEDIA_ROOT, 'blast_db/protein/ZJLY_hap1.pep')
        },
        'command': 'blastp'
    },
}