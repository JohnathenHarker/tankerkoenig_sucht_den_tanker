set table "template_Article.pgf-plot.table"; set format "%.5f"
set format "%.7e";; set samples 25; set dummy x; plot [x=-5:5]  a = 0.9 f(x) = a * sin(x) g(x) = a * cos(x) plot f(x) ;
