// A simple script to dump sudokus from samurai_sudoku.com


function dump_samurai() {
    s = "\n";
    for (var i = 0; i < 21; i++) {
        for (var j = 0; j < 21; j++) {

            if ( (i <  6 && j > 8 && j < 12) ||
                (i > 14 && j > 8 && j < 12) ||
                (j <  6 && i > 8 && i < 12) ||
                (j > 14 && i > 8 && i < 12) ) {
                s += " ";
            } else {
                if (e[i][j] == 0)
                    s += ".";
                else
                    s += e[i][j];
            }
        }
        s += "\n";
    }
    return s;
}


dump_samurai();