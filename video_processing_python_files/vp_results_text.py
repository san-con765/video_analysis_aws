# Example:
# Score: 100/100 
 
#  You're a Natural! You're showing strong adherence to the recommended shoulder exercises
#  To improve try to ...


def textResults(results):
    print("Run Process textResults")
    # Results in format results[found, top = x, bottom = x, speed = x]

    if results[0] == 0:
        result = "Unable to identify... \n \n Try to do ..."
        return result
    else:
        total = results[1] + results[2] + results[3]
        if total == 1:
            result = "Score: 50/100 \n \n Good job! You're on your way to improve your shoulder mobility."
        elif total == 2:
            result = "Score: 75/100 \n \n Great job! You're showing strong adherence to the recommended shoulder exercises"
        else:
            result = "Score: 100/100 \n \n You're a Natural! You're showing strong adherence to the recommended shoulder exercises"

        #  \n \n You’re currently completing the exercise too quickly! Consider slowing down and counting 3 seconds as you go up, and 3 seconds as you go down."
        
        
    # Review bttom of rep - fully extended arms
    result += "\n To improve try to ..."
    if results[1] == 1:
        result += "\n- To improve try to ensure that your arms are completely straight when reaching towards the sky. The goal is to be close if not completely straight."
    elif results[1] == 2:
        result += "\n- You're doing a great job, but your arms are slightly bent at the top of the repition, try to ensure they are almost if not completely straight."
    elif results[1] == 3:
        result += "\n- Great job extending your arms, doing great!"
    else:
        # result += "Something went wrong identifying the bottom of the repition"
        print("Something went wrong, currently receiving a ",results[1], "output for the bottom of rep which should not be possible." )

    # Review bottom of rep - arms accurately bent
    if results[2] == 1:
        result += "\n- To improve try to ensure that your arms are at 90 degree at the bottom of the repition."
    elif results[2] == 2:
        result += "\n- Good effort but try to make sure you're bringing your arms further down and are closer to a ring angle at the bottom of the rep."
    elif results[2] == 3:
        result += "\n- Awesome job, the bottom of the repition is exactly what we are looking for!"
    else:
        # result += "FAILED"
        print("Something went wrong, currently receiving a ",results[2], "output for the bottom of rep which should not be possible." )

    if results[3] == 1:     # Too fast
        result += "\n- Try to slow down during the repition, it should be around 2 seconds going up and 2 seconds going down."
    elif results[3] == 2:   # Too slow
        result += "\n- Try to speed up a little during the repition, it should be around 2 seconds going up and 2 seconds going down."
    elif results[3] == 3:   # Just right
        result += "\n- Perfect! Moving just at the right speed!"
    else:
        # result += "FAILED"
        print("Something went wrong, currently receiving a ",results[3], "output for the bottom of rep which should not be possible." )
            
    return result
        
