import gc

import time
# gc.collect()
# import board
gc.collect()
# import demos
# import nightlight
# gc.collect()
# import rainbowdemo
# gc.collect()

# COMMENT THIS IN WHEN YOU WANT TO PROGRAM THE LEFT HAND SIDE
# import left_chest
# gc.collect()

# COMMENT THIS IN WHEN YOU WANT TO PROGRAM THE RIGHT HAND SIDE
import right_chest
gc.collect()

# import blinkdemo
# from buttonwatcher import ButtonWatcher
# gc.collect()

index = 0
demos = [
    # left_chest.LeftUnit(),
    right_chest.RightUnit(),
    # nightlight.NightLight(),
    # blinkdemo.FlashDemo(),
    # rainbowdemo.RainbowDemo(),
    # rainbowdemo.RainbowCycleDemo(),
    # blinkdemo.BlinkDemo(),
    # demos.TouchDemo(),
]

currentDemo = demos[index]
demos[index].start()

# buttonA = ButtonWatcher(board.BUTTON_A)
# buttonB = ButtonWatcher(board.BUTTON_B)


while True:
    previousIndex = index

    # if buttonA.wasPressed():
    #     index += 1
    # if buttonB.wasPressed():
    #     index -= 1

    index %= len(demos)

    if previousIndex != index:
        for demo in demos:
            demo.stop()
        currentDemo = demos[index]
        currentDemo.start()

    currentDemo.next()
    time.sleep(0.001)
