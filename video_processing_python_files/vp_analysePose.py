import mediapipe as mp
import cv2
import os
import video_processing_python_files.vp_saveImages

# Local modules to be include
import video_processing_python_files.vp_calculateAngle

# Identify the first repition 
# Is done by identifying when the wrist is first identified above the shoulders
def IdentifyFirstRep(AnalysisArray):
    print("Run Process identifyFirstRep")
    print("Identify First Rep")

    #Go through each item in the array - first rep is identified when the wrist is put above the shoulder.
    for x in range(0,len(AnalysisArray)):
        wrist_y = AnalysisArray[x][4][1]
        shoulder_y = AnalysisArray[x][2][1]
        if wrist_y < shoulder_y:
            # Return the frame (image) and the index
            print("First rep at ", x)
            return x, x
    # This will cause an error message - if time is available include information around 
    return 0, 0
    
# Identify the max height of the reptition
# Is done by identifying when the wrist is at the highest point
def IdentifyMaxofRep(AnalysisArray):
    print("Run Process IdentifyMaxofRep")
    print("Start IdentifyMaxofRep")
    max_height = float('inf')  
    max_frame = None
    max_index = -1

    # print("Test Now")
    for x in range(0,len(AnalysisArray) - 11, 10): 
        print("Test Begins")
        print("Max Test ", x, " / ", len(AnalysisArray)) 
        # SaveImage(AnalysisArray[x][0], "max Compare 1 " + "wrist_1 x=" + str(x) + ".jpg")
        wrist_1 = AnalysisArray[x][4][1]
        # SaveImage(AnalysisArray[x+5][0], "max Compare 2 " + "wrist_1 x=" + str(x+5) + ".jpg")
        wrist_2 = AnalysisArray[x + 5][4][1]
        print("wrist 1 = ", wrist_1)
        print("wrist 2 = ", wrist_2)

        if wrist_1 < wrist_2:
            print("wrist Test = True")
            max_height = wrist_1
            max_frame = AnalysisArray[x][0]
            max_index = x
            # print(x) 
            return x - 10, x+5
        # else:
            # print("wrist Test = True")
    
    # print("This finished")
    

    return 0, len(AnalysisArray) -1
    

# Identify the max height of the reptition
# Is done by identifying when the wrist is at the highest point
def IdentifyMinofRep(AnalysisArray):
    print("Run Process IdentifyMinofRep")
    print("Start IdentifyMinofRep")
    max_height = float('inf')  
    max_frame = None
    max_index = -1

    # print("Test Now")
    for x in range(0,len(AnalysisArray) - 11, 5): 
        print("Test Begins")
        print("Min Test ", x, " / ", len(AnalysisArray)) 
        # SaveImage(AnalysisArray[x][0], "Min Compare 1 " + "wrist_1 x=" + str(x) + ".jpg")
        wrist_1 = AnalysisArray[x][4][1]
        # SaveImage(AnalysisArray[x+5][0], "Min Compare 2 " + "wrist_1 x=" + str(x+5) + ".jpg")
        wrist_2 = AnalysisArray[x + 5][4][1]
        # print("wrist 1 = ", wrist_1)
        # print("wrist 2 = ", wrist_2)

        if wrist_1 > wrist_2: # or wrist_1 < AnalysisArray[x][2][1]: #Shoulder
            print("wrist Test = True")
            max_height = wrist_1
            max_frame = AnalysisArray[x][0]
            max_index = x
            # print(x) 
            return x-10, x+5
        # else:
            # print("wrist Test = True")
    
    # print("This finished")
    return 0, len(AnalysisArray) -1
    
    
def AnalyseRepetitions(AnalysisArray):
    #Initiation of start Analysis
    ResultsArray = []
    GoingUp = True
    SaveFrame, CheckPoint = IdentifyFirstRep(AnalysisArray)
    if CheckPoint == 0:
        return 0
    video_processing_python_files.vp_saveImages.SaveImage(AnalysisArray, SaveFrame, filename="image_1.jpg")
    ResultsArray.append(1)
    ResultsArray.append(CheckPoint)
    print("Results Array = ",ResultsArray)
    
    print("Begin Analysis")
    AnalysisArray = AnalysisArray[CheckPoint:len(AnalysisArray) -1 ]
    
    while CheckPoint != 0:
        
        if GoingUp:
            print("")
            print("Test Going Up")
            print("CheckPoint = ", CheckPoint)
            print("len(AnalysisArray)-1  = ", len(AnalysisArray)-1 )
            SaveFrame, CheckPoint = IdentifyMaxofRep(AnalysisArray[CheckPoint:len(AnalysisArray)-1 ])
            if CheckPoint > len(AnalysisArray) -2 :
                return 0
            video_processing_python_files.vp_saveImages.SaveImage(AnalysisArray,SaveFrame, filename="image_3.jpg")
            # ReptitionCounter +=1
            ResultsArray.append(CheckPoint + ResultsArray[0])
            print("Results Array = ",ResultsArray)
            GoingUp = False
            AnalysisArray = AnalysisArray[CheckPoint:len(AnalysisArray)-1 ]
            print("Going up done)")
        else:
            print("")
            print("Test Going Down")
            print("CheckPoint = " ,CheckPoint)
            print("len(AnalysisArray)-1  = ", len(AnalysisArray)-1 )
            print("Test")
            SaveFrame, CheckPoint = IdentifyMinofRep(AnalysisArray[CheckPoint:len(AnalysisArray)-1 ])
            if CheckPoint >= len(AnalysisArray) -1 :
                return 0
            video_processing_python_files.vp_saveImages.SaveImage(AnalysisArray, SaveFrame, filename="image_2.jpg")
            ResultsArray.append(CheckPoint+ ResultsArray[1])
            print("Results Array = ",ResultsArray)
            print("Going down done")
            
            
            return ResultsArray
            
            
        
        print("Up to ", CheckPoint, " / ", len(AnalysisArray) -1 )

    return 0



def AnalysePose(video_path):
    print("Run Process AnalysePose")
    print("Start Analysing Analyse Pose")
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    print("Initialise MP")

    AnalysisArray = []
    ResultsArray = []

    cap = cv2.VideoCapture(video_path)

    #TESTING TO CALCULATE FRAMES IN VIDEO
    # Assuming 'cap' and 'video_path' are already defined as shown in your screenshot
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_name = os.path.basename(video_path)
    frame_number = 0
    
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        print("Run MP")
        ##print("Flag 1")
        while cap.isOpened() or frame_number <300:


            #TESTING
            frame_number += 1
            print(f"{video_name} - Frame {frame_number} / {total_frames}")


            #print("Flag 2")
            ret, frame = cap.read()
            
            #Cuts at frame > 200 for processing issues
            if not ret or frame_number > 150:
                print("End of video.")
                #print("Flag 3")
                break

            #print("Flag 4")
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            # print("Process Image")

            #print("Flag 5")
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #print("Flag 6")

            
            # print("Identify Landmarks")
            try:
                #print("Flag 7")
                
                landmarks = results.pose_landmarks.landmark
                shoulder = (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image.shape[1],
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image.shape[0])
                elbow = (landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image.shape[1],
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image.shape[0])
                wrist = (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * image.shape[1],
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * image.shape[0])
                
                # print("Calculate Angles")
                angle = video_processing_python_files.vp_calculateAngle.calculate_angle(shoulder, wrist, elbow)
                # print(image.shape)
                # print("Angle = ", angle)
                # print("Shoulder = ",shoulder )
                # print("Shoulder X = ", landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x)
                # print("Shoulder Y = ", landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y)

                # print("Elbow = ",elbow )
                # print("Elbow X = ",landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y )
                # print("Elbow Y = ",elbow )
                # print("Wrist = ",wrist )
                # print("Wrist X = ",landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x )
                # print("Wrist Y = ",landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y )

                # Would show the angle on screen
                # cv2.putText(image, str(round(angle, 2)), 
                #             [500,500],
                #             cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 3, cv2.LINE_AA)
                
                
                AnalysisArray.append([image, angle, shoulder, elbow, wrist])
                ResultsArray.append([angle, shoulder, elbow, wrist])
                #print("Flag 8")


            
            except Exception as e:
                # #print("Flag 9")
                print(e)
                pass

            # ##print("Flag 10")


            # print("Draw on image")
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                                      mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))

            # cv2.imshow('Mediapipe Feed', image)
            # time.sleep(1)  # Wait for 1 second between each frame

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        print("Finish Analysis")
        # print(AnalysisArray[0])

        ##USE ANALYSIS ARRAY TO CAPTURE EACH FRAME
        resultsArrayOutput = (AnalyseRepetitions(AnalysisArray))
        

        # Used to generate response text
        ResultsText = []

        # If results did not finish return 0
        print("Scenario Testing")
        
        # Print checkpoint Locations
        print(resultsArrayOutput)

        ############### AnalysisArray === [image, angle, shoulder, elbow, wrist]) ###############

        # Print elbow angle
        print(AnalysisArray[resultsArrayOutput[0]][1])

        # Print Shoulder Location
        print(AnalysisArray[resultsArrayOutput[0]][2])

        # Elbow Location Shoulder Location
        print(AnalysisArray[resultsArrayOutput[0]][3])
        print("Test length of ResultsArray ", len(ResultsArray))
        

        try:
            
            if resultsArrayOutput[0] == 0:
                return [0, 1, 1, 1]
            else:
                print("Test length of each frame ")
                frame1 = resultsArrayOutput[0]
                frame2 = resultsArrayOutput[0] + resultsArrayOutput[1]
                frame3 = resultsArrayOutput[0] + resultsArrayOutput[1] + resultsArrayOutput[2]
                print(frame1)
                print(frame2)
                print(frame3)

                # Scenario 1 - Failure to detect user
                
                ResultsText.append(1)
                # return AnalysisArray, ResultsText
                    
                # Scenario 2 - Identify top of arm
                print("Top arm test = ", ResultsArray[frame2][0])
                if ResultsArray[frame2][0] <60:
                    ResultsText.append(3)
                elif ResultsArray[frame2][0] <70:
                    ResultsText.append(2)
                else:
                    ResultsText.append(1)
                print("Resulted in ", ResultsText)

                # Scenario 3 - Bottom of arm
                print("Bottom arm test = ", ResultsArray[frame3][0])
                if 55 < ResultsArray[frame3][0] <110:
                    ResultsText.append(3)
                elif ResultsArray[frame3][0] >109:
                    ResultsText.append(2)
                else:
                    ResultsText.append(1)
                print("Resulted in ", ResultsText)

                # Scenario 4 - time
                speed = frame2 + frame3 - frame1
                print("Speed Test = ", speed)
                if  speed < 60 : #Too Fast
                    ResultsText.append(1)
                elif speed > 145: #Too Slow
                    ResultsText.append(2)
                else:
                    ResultsText.append(3)
                print("Resulted in ", ResultsText)
        except Exception as e:
                # #print("Flag 9")
                print("SOMETHING HERE FAILED")
                print(e)
            

        print("Results Text = ",ResultsText)
        print("Results Score = ", ResultsText[0] + ResultsText[1] + ResultsText[2])



        return AnalysisArray, ResultsText
        # AnalysisArray (need to find a way of providing the three frames required), Results (in format of [1,2,2,2])



    # UpdatedArray = AnalysisArray


#LOCAL
# videoExample = "/Users/seanryan/Downloads"
# AnalysePose(videoExample)

