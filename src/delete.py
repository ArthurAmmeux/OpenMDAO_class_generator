def delete_var(result, index):
    i = 0
    for g in result:
        for c in g[1]:
            for j in range(len(c.var_in)):
                if i == index:
                    c.var_in[j].delete()
                    c.var_in.remove(c.var_in[j])
                i += 1
            for k in range(len(c.var_out)):
                if i == index:
                    c.var_out[k].delete()
                    c.var_out.remove(c.var_out[k])
                i += 1
