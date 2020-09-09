def load(cc):
    # TODO: loop throught main blocks save data to csv
    view = cutie.get_input(cc.value('load', 'whichview'))
    cutie.cprint('info', cc.value('git-talk', 'wait'))
    ld = load_dataset.LoadData(view)
    error = ld.get_objects()
    if error == 0:
        #stmt, obj_list = load_dataset.get_objects(view)
        if ld.obj_list is not None:
            captions = [0]
            cutie.cprint('info', cc.value('load', 'pick_main_table'))
            main_obj = cutie.select_propmt(
                cc.value('load', 'object_list'), ld.obj_list, captions)
            if not cutie.get_exit(main_obj):
                rd_cnt = cutie.get_number(
                    cc.value('load', 'how_many'), min_value=1, allow_float=False)
                cutie.cprint('wait', (cc.value('git-talk', 'wait')))
                # run main_obj first, then loop rest
                cutie.cprint('info', (ld.build_sql))
                # TODO: save into csv
                mtb = main_obj.strip().split(' ')[0]
                r = ld.get_result(mtb, rd_cnt)
                f = mtb + '.csv'
                with open(f, 'w') as c:
                    wr = csv.writer(c)
                    wr.writerow(r)
                    cutie.cprint('info', ('write into ', f))
                cutie.cprint('info', mtb, '--row count--->', len(r))
                # print(r[0])
                cutie.cprint('done', (cc.value('git-talk', 'done')))
    else:
        cutie.cprint('alarm', cc.value('load', 'no_table'))
        # cutie.get_exit()
