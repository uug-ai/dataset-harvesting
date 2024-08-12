
from utils.TranslateObject import translate
from utils.VariableClass import VariableClass
import cv2
import time

# Initialize the VariableClass object, which contains all the necessary environment variables.
var = VariableClass()

# Function to process the frame.


def processFrame(MODEL, frame, video_out):
    # Perform object classification on the frame.
    # persist=True -> The tracking results are stored in the model.
    # persist should be kept True, as this provides unique IDs for each detection.
    # More information about the tracking results via https://docs.ultralytics.com/reference/engine/results/

    total_time_class_prediction = 0
    if var.TIME_VERBOSE:
        start_time_class_prediction = time.time()

    # Execute the model
    results = MODEL.track(
        source=frame,
        persist=True,
        verbose=False,
        conf=var.CLASSIFICATION_THRESHOLD)

    if var.TIME_VERBOSE:
        total_time_class_prediction += time.time() - start_time_class_prediction

    # ###############################################
    # This is where the custom logic comes into play
    # ###############################################
    # Check if the results are not None,
    #  Otherwise, the postprocessing should not be done.
    # Iterate over the detected objects and their masks.

    annotated_frame = frame.copy()

    # Empty frame containing labels with bounding boxes
    labelsAndBoxes = []

    if results is not None:

        # Using the results of the classification, we can verify if we have a condition met.
        # We can look for example for people who are:
        # - not wearing a helmet,
        # - people with a blue shirt,
        # - cars driving in the opposite direction,
        # - etc.
        # You are in the driving seat so you can write your custom code to detect the condition
        # you are looking for.

        is_condition_met = False
        # Write your function here or custom code and set is_condition_met to True if the condition is met.
        # is_condition_met = condition(results)
        # labelsAndBoxes = ....

        if is_condition_met:
            print("Condition met, we are gathering the labelsAndBoxes and return results")
            return frame, total_time_class_prediction, True, labelsAndBoxes
        else:
            print("Condition not met")

        # Annotate the frame with the classification objects.
        # Draw the class name and the confidence on the frame.
        if var.SAVE_VIDEO or var.PLOT:
            for box, mask in zip(results[0].boxes, results[0].masks or [None] * len(results[0].boxes)):
                # Translate the class name to a human-readable format and display it on the frame.
                object_name = translate(results[0].names[int(box.cls)])
                cv2.putText(
                    img=annotated_frame,
                    text=object_name,
                    org=(int(box.xyxy.tolist()[0][0]), int(
                        box.xyxy.tolist()[0][1]) - 10),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 255, 0),
                    thickness=2)

                # Draw the bounding box on the frame.
                cv2.rectangle(
                    img=annotated_frame,
                    pt1=(int(box.xyxy.tolist()[0][0]), int(
                        box.xyxy.tolist()[0][1])),
                    pt2=(int(box.xyxy.tolist()[0][2]), int(
                        box.xyxy.tolist()[0][3])),
                    color=(0, 255, 0),
                    thickness=2)

    # Depending on the SAVE_VIDEO or PLOT parameter, the frame is annotated.
    # This is done using a custom annotation function.
    if var.SAVE_VIDEO or var.PLOT:

        # Show the annotated frame if the PLOT parameter is set to True.
        cv2.imshow("YOLOv8 Tracking",
                   annotated_frame) if var.PLOT else None
        cv2.waitKey(1) if var.PLOT else None

        # Write the annotated frame to the video-writer if the SAVE_VIDEO parameter is set to True.
        video_out.write(
            annotated_frame) if var.SAVE_VIDEO else None

    return frame, total_time_class_prediction, False, labelsAndBoxes
