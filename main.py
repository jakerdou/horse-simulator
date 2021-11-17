# 1. calibrate distance measurements
    # ask user for user_height
    # tell user to stand a certain distance (2 feet?) away from the camera
    # sleep(5) (wait 5 seconds for person to get in position)
    # capture number of pixels tall the person is
    # using height and number of pixels, calculate focal_length

# 2. pop up GUI
    # 2a. shootaround mode is clicked
        # start video feed
        # while cancel is not pressed
            # if person is detected in video feed
                # turn LED green
                # if shot is detected in video feed
                    # calculate distance of person
                    # turn LED red
                    # sleep(5) (wait 5 seconds)
                    # if distance sensor detected object less than certain distance (6 inches?) away
                        # count shot as made
                    # else
                        # count shot as missed
        # display shot chart
        # return to home menu

    # 2b. single player mode is pressed
        # start video feed
        # shots missed = 0
        # shots made = 0
        # turn LED red
        # while cancel is not pressed and shots missed < 5
            # select distance for shot to be taken
            # if person detected in video feed
                # if person is correct distance away
                    # turn LED green
                    # if shot is detected in video feed
                        # calculate distance of person
                        # turn LED red
                        # sleep(5) (wait 5 seconds)
                        # if distance sensor detected object less than certain distance (6 inches?) away
                            # shots made ++
                        # else
                            # shots missed ++
        # display shots made (score)
        # return to home menu
