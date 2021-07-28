import os
import re
import sys
import time
import gzip
import subprocess
import pandas as pd
import click

def guide_cell_barcode_vs_all_cell_barcode(df_in, guide_in):
    guide_boolean = df_in['guide'] == guide_in
    cells_with_guide = len(df_in[guide_boolean]['cell_barcode'].unique())
    all_cells = len(df_in['cell_barcode'].unique())
    return [str(guide_in), cells_with_guide, all_cells]

@click.command()
@click.argument('filename', type=click.Path(exists=True), nargs=1)
@click.argument('filename_out', nargs=1)
@click.argument('guides_list', nargs=-1)
def main(filename, filename_out, guides_list):
    click.echo('Generating summary statistics for ' + str(filename))
    click.echo('For the guides ' + ", ".join(guides_list))
    df = pd.read_csv(filename,sep="\t", names=['label', 'cell_barcode', 'guide_seq', 'guide'], dtype={'label': str, 'cell_barcode':str, 'guide_seq':str, 'guide':str})
    results_out = [guide_cell_barcode_vs_all_cell_barcode(df, guide_i) for guide_i in guides_list]
    df_out = pd.DataFrame(results_out, columns = ['guide', 'cell_with_guide', 'total_cell_count'])
    df_out.to_csv(filename_out, sep="\t")
if __name__ == '__main__':
    main()


    