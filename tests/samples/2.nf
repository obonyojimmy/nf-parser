include { foo; bar } from './module/1.nf'

params.query = "$baseDir/data/sample.fa"
params.db = "$baseDir/blast-db/pdb/tiny" // path to db folder
params.out = "result.txt"
params.chunkSize = 100 // the chunk size

def foo() {
    'Hello world'
}

def bar(alpha, omega) {
    alpha + omega
}

process align {
    publishDir "${params.outdir}", mode: 'copy'
    
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
    if(1 == 1)
    // script comment
        """
        t_coffee -in $sequences > out_file
        """

    else if(2 == 2)
        """
        mafft --anysymbol --parttree --quiet $sequences > out_file
        """

}

workflow  { 
    data = channel.fromPath('/some/path/*.txt')
    foo()
    bar(data)
}