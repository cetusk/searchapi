
#########################################################
# >>> assertions

def assertionchecking_logging(message:str, logger:dict):
    if __debug__:
        assert type(message) == str, "Irregal type of message."
        if logger:
            assert type(logger) == dict, "Irregal type of a logger."
            assert type(logger["counter"]) == list, "Irregal type of a logger.counter."
            assert len(logger["counter"]) > 0, "No buffer of the logger.counter."
            assert type(logger["counter"][0]) == int, "Irregal value type of the logger.counter."
            assert type(logger["overwrite"]) == bool, "Irregal type of the logger.overwrite."

def assertionchecking_search(modulename:str, keyname:str, maxdepth:int, strict:bool, logger:dict):
    assert type(modulename) == str, "Irregal type of modulename."
    assert type(keyname) == str, "Irregal type of keyname."
    assert type(maxdepth) == int, "Irregal type of maxdepth."
    assert type(strict) == bool, "Irregal type of strict flag."
    assert maxdepth >= 0, "Irregal value of maxdepth."
    if logger:
        assert type(logger) == dict, "Irregal type of a logger."
        assert type(logger["counter"]) == list, "Irregal type of a logger.counter."
        assert len(logger["counter"]) > 0, "No buffer of the logger.counter."
        assert type(logger["counter"][0]) == int, "Irregal value type of the logger.counter."
        assert type(logger["overwrite"]) == bool, "Irregal type of the logger.overwrite."


#########################################################
# >>> logging function

def logging(message:str, logger:dict=None):
    assertionchecking_logging(message, logger)
    if __debug__:
        if logger:
            logger["counter"][0] += 1
            if logger["overwrite"]:
                print("[%d]: %s" % (logger["counter"][0], message), end=" "*32+"\r")
            else:
                print("[%d]: %s" % (logger["counter"][0], message))
        else:
            print(message, end=" "*32+"\r")


#########################################################
# >>> search API
def search(modulename:str, keyname:str, maxdepth:int=3, strict:bool=False, logger:dict=None):
    assertionchecking_search(modulename, keyname, maxdepth, strict, logger)
    try:
        # API list
        apilist = []
        accuracies = []
        # search depth
        splitted_modulename = modulename.split(".")
        depth = len(splitted_modulename) - 1

        # stop when search depth approached to maxdepth
        if depth > maxdepth:
            return ([], [])

        # tbd
        exec("import %s" % splitted_modulename[0])

        # get hierarchy
        hierarchy = eval("dir(%s)" % modulename)

        # sweep for hierarchy
        logging("Searching under %s ..." % modulename, logger=logger)
        for submodulename in hierarchy:
            # ----->>> igore case
            # ignore a name / case-1: not module type
            try:
                exec("type(%s.%s)" % (modulename, submodulename))
            except:
                continue
            # ignore a name / case-2: unreadable "_X"
            if submodulename[0] == "_":
                continue
            # ignore a name / case-3: recursivable "__X__"
            if len(submodulename) > 4:
                if submodulename[:2] == "__" and submodulename[-2:] == "__":
                    continue
            # ignore a name / case-4: recursivable "dir(X) == dir(X.Y)"
            if eval("dir(%s.%s)" % (modulename, submodulename)) == hierarchy:
                continue

            # ----->>> pattern matching
            # pattern match: regiater the keyname and accuracy of correspondence
            if strict:
                # strict
                if keyname in submodulename:
                    apilist.append(keyname)
                    accuracies.append( float(len(keyname))/float(len(submodulename)) )
            else:
                # not strict
                if keyname.lower() in submodulename.lower():
                    apilist.append("%s.%s" % (modulename, submodulename))
                    accuracies.append( float(len(keyname))/float(len(submodulename)) )
            
            # ----->>> next search and concatenete subresult
            (buffer_apilist, buffer_accuracies) = search(modulename="%s.%s" % (modulename, submodulename), keyname=keyname, maxdepth=maxdepth, strict=strict, logger=logger)
            if len(buffer_apilist) > 0:
                apilist += [ " -- " + b for b in buffer_apilist ]
                accuracies += buffer_accuracies

    except KeyboardInterrupt:
        if depth == 0:
            logging("STOP: Keyboard interruptted.", logger)
            return False
        else:
            return ([], [])
    except Exception as e:
        logging("ERROR [depth=%d] (module=%s.%s): %s." % (depth, modulename, submodulename, e), logger)
        if depth == 0:
            return False
        else:
            return ([], [])
    else:
        if depth == 0:
            logging("Successfully finished.", logger)
            # ----->>> display result
            print("")
            stdout = "".join([ "%s ( accuracy: %.1f %% )\n" % (api, acc*100.0) for (api, acc) in zip(apilist, accuracies) ])
            print(stdout)
            print("")
            return True
        else:
            return (apilist, accuracies)


#########################################################
# >>> test
if __name__ == "__main__":
    logs = { "counter": [0], "overwrite": True }
    search(modulename="numpy", keyname="full", logger=logs)
