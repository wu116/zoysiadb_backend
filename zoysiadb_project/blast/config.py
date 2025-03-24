import os
from django.conf import settings

BLAST_CONFIG = {
    'blastn': {
        'databases': {
            'human': '/blast_db/human_genome.fa',
            'mouse': '/blast_db/mouse_genome.fa'
        },
        'command': 'blastn'
    },
    'blastp': {
        'databases': {
            'protein': os.path.join(settings.MEDIA_ROOT, 'blast_db/protein/ZJLY_hap1.pep')
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