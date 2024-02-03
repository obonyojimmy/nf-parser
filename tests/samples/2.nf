include { foo; bar } from './module/1.nf'

params.query = "$baseDir/data/sample.fa"
params.db = "$baseDir/blast-db/pdb/tiny" // path to db folder
params.out = "result.txt"
params.chunkSize = 100 // the chunk size

scores_files_py = collect { "'${it}'" }

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
    path "${tsv.simpleName}_scores.tsv", emit: scores, something: bar

    // a comment
    script:
    // script comment
    // script comment
    def scores_files_py = scores_files.collect { "'${it}'" }
    def hits_files_py = collect { "'${it}'" }.join(", ")
    if(1 == 1)
        """
        t_coffee -in $sequences > out_file
        """
    
    else if(2 == 2) {
        """
        mafft --anysymbol --parttree --quiet $sequences > out_file
        """
    }
}

workflow  { 
    data = channel.fromPath('/some/path/*.txt')
    foo()
    bar(data)
}