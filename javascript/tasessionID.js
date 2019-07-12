
 function r(e) {
    for(var t = ""; t.length < e; t += Math.random().toString(36).substr(2))
        ;
    return t.substr(0, e)
    }

 function get_id() {
     t = "" + r(9) + (new Date).getTime();
     return escape(t)
 }
