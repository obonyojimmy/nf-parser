#!/usr/bin/env nextflow
 
/*
 * Defines the pipeline input parameters (with a default value for each one).
 * Each of the following parameters can be specified as command line options.
 */
params.query = "$baseDir/data/sample.fa"
params.db = "$baseDir/blast-db/pdb/tiny"
params.out = "result.txt"
params.chunkSize = 100
 
db_name = file(params.db).name
db_dir = file(params.db).parent
scores_files_py = collect { "'${it}'" }

nextflow.enable.dsl=2

//include { foo } from './module/1.nf'
//include { BAR } from './module/2.nf'

db_name = file(params.db).name

//def sayHello() {
//    println "$params.foo $params.bar"
//}

Channel.fromPath(params.query)

/*
 * Defines the pipeline input parameters (with a default value for each one).
 * Each of the following parameters can be specified as command line options.
 */
params.in = "$baseDir/data/sample.fa" // path to fa file
// some comment
params.query = "$baseDir/data/sample.fa"
params.db = "$baseDir/blast-db/pdb/tiny"
params.out = "result.txt"
params.chunkSize = 100

process foo {
    container 'python'

    output:
    path 'sample.txt'

    script:
    // script comment
    '''
    echo 'hello' >  sample.txt
    '''
}

workflow  { 

    foo()
}

workflow jimmy {
    foo()
    /*
     * Create a channel emitting the given query fasta file(s).
     * Split the file into chunks containing as many sequences as defined by the parameter 'chunkSize'.
     * Finally, assign the resulting channel to the variable 'ch_fasta'
     */
    Channel
        .fromPath(params.query)
        .splitFasta(by: params.chunkSize, file:true)
        .set { ch_fasta }
    
    /*
     * Execute a BLAST job for each chunk emitted by the 'ch_fasta' channel
     * and emit the resulting BLAST matches.
     */
    ch_hits = blast(ch_fasta, db_dir)
 

    // define a channel emitting three values
    source = Channel.of( 'alpha', 'beta', 'delta' )
    
    
    /*
     * Execute a BLAST job for each chunk emitted by the 'ch_fasta' channel
     * and emit the resulting BLAST matches.
     */
    ch_sequences
        .collectFile(name: params.out)
        .view { file -> "matching sequences:\n ${file.text}" }
    
    Channel
        .watchPath( '/path/*.fa' )
        .subscribe { println "Fasta file: $it" }

    Channel
        .watchPath( '/path/*.fa', 'create,modify' )
        .subscribe { println "File created or modified: $it" }

    
    Channel
        .fromPath(params.query)
        .branch{ }
        .splitFasta(by: params.chunkSize, file:true)
        .splitFasta{ }
        .set{ ch_fasta }
        .collect()
        .view { file -> "matching sequences:\n ${file.text}" }

    ch_hits = blast(ch_fasta, db_dir)
        
 
}
