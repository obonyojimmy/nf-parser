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