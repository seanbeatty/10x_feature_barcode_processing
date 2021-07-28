import pysam
import click

def parse_read(sam_file_line):
    out_dict = {'qname':sam_file_line.query_name, 'cell_barcode':'NA', 'feature_barcode':'NA', 'feature_index':'NA'}
    tags = dict(sam_file_line.tags)
    try:
        out_dict['cell_barcode'] = tags['CB'] 
    except KeyError:
        out_dict['cell_barcode'] = 'NA'
    try:
        out_dict['feature_barcode'] = tags['fb']
    except KeyError:
        out_dict['feature_barcode'] = 'NA'
    try:
        out_dict['feature_index'] = tags['fx']
    except KeyError:
        out_dict['feature_index'] = 'NA'
    return out_dict['qname'], out_dict['cell_barcode'], out_dict['feature_barcode'], out_dict['feature_index']

@click.command()
@click.argument('bam_path', nargs=1,type=click.Path(exists=True))
@click.argument('out_path', nargs=1)
def main(bam_path,out_path):
    samfile = pysam.AlignmentFile(bam_path, "rb") 
    with open(out_path, 'a') as the_file:
        i = 1 
        lines = []
        for line in samfile:
            line_to_add = "\t".join(parse_read(line))
            line_to_add = line_to_add + "\n"
            the_file.write(line_to_add)




if __name__ == "__main__":
    main()