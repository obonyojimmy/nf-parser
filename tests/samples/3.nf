#!/usr/bin/env nextflow
nextflow.enable.dsl=2

include { flow1 } from './module/1.nf'
include { flow2 } from './module/2.nf'

params.in = "$baseDir/data/sample.fa"
// params.module_dir = '.'
params.cachedir = '/path/to/cache' // the path to blah
params.cores = 40
params.pdb = '/path/to/pdp/abc.pdb'


process foo {
    container 'python:latest'
    containerOptions '--volume /data:/data'

    output:
    path 'output.txt'

    shell:
    '''
    cat --data  > output.txt
    '''
}

process coffee {
    input:
    path sequences

    script:
    if( mode == 'tcoffee' )
        """
        t_coffee -in $sequences > out_file
        """

    else if( mode == 'mafft' )
        """
        mafft --anysymbol --parttree --quiet $sequences > out_file
        """

}

process baz {
    // a comment
    // a comment
    storeDir "${params.cachedir}/${pdb.baseName}"
    publishDir "${params.outdir}", mode: 'copy'

    input:
    // some comment
    /* file input_file */
    file input_file

    output:
    // output comment
    // output comment2
    file output

    script:
    // c1
    // c1
    """
    awk '/^>/{f="seq_"++d} {print > f}' < input.fa
    touch output.txt
    touch output.txt
    touch output.txt
    """
    // c2
    // c3
}

process align {
    input:
    // some comment
    /* file input_file */
    file input_file

    output:
    // output comment
    // output comment2
    file output

    // a comment
    script:
    // script comment
    if(1 == 1)
    
        """
        t_coffee -in $sequences > out_file
        """

    else if(2 == 2)
        """
        mafft --anysymbol --parttree --quiet $sequences > out_file
        """

}
 
workflow  {
    foo()
}

workflow jimmy  {
    coffee()
    baz(flow1.out)
}