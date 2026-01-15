function q(b, e, c) {
    if (!e)
        return b;
    -1 < b.indexOf("{") && (b = "");
    for (var a = b.split("&"), f, d = !1, h = !1, g = 0; g < a.length; g++)
        f = a[g].split(":"),
        f[0] == e ? (!c || d ? a.splice(g, 1) : (f[1] = c,
        a[g] = f.join(":")),
        h = d = !0) : 2 > f.length && (a.splice(g, 1),
        h = !0);
    h && (b = a.join("&"));
    !d && c && (0 < b.length && (b += "&"),
    b += e + ":" + c);
    return b
}
function sdk(tag_value){
    // 第一次
    e = `s-${tag_value}|${+new Date}` // 文档值 var ue_id = '1XH96MCCP5AJE1VBZ31Y'
    a = q("{}", "tb", e)
    a = q(a, "t", +new Date)
    // 第二次
    a = q(a, "adb", "adblk_no")
    a = q(a, "t", +new Date)
    // 第三次
    e = `${tag_value}+s-${tag_value}|${+new Date}` // 文档值 var ue_id = '1XH96MCCP5AJE1VBZ31Y'
    a = q(a, "tb", e)
    a = q(a, "t", +new Date);
    return a
    // 会返回session-token
}
//  匹配 var ue_id = '(.*?)'
