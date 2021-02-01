import time
import os
from psychopy import visual, core, event, data
from psychopy.hardware import keyboard
from pylsl import StreamInfo, StreamOutlet # For sending markers
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from random import randrange


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session, Usually created by psychopy
expInfo = {'participant': '', 'session': '001'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = 'visual_oddball'

##########################################
# Experiment params
##########################################
N = 1 # N number of trials
M = 5 # each trial consist of M objects
oddNumList = [randrange(2,M) for p in range(N)] # The 3rd-Mth obj is an oddball


#create a window
mywin = visual.Window([800,600],monitor="macMonitor", units="deg")
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = mywin.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
	expInfo['frameRate'] = 60.0
	frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize Marker stream
startClock = core.Clock()
info = StreamInfo('visual_oddball_Mrkrs', 'Markers', 1, 0.0, 'int32','marker')
outlet = StreamOutlet(info)
outlet.push_sample([-1], time.time())

##########################################
# Define object to be used in experiment
##########################################
# Green Circle
circleG = visual.Circle(
    win=mywin,
    autoDraw = False,
    units="pix",
    radius=150,
    fillColor=[0, 1, 0],
    lineColor=[-1, -1, -1],
    edges=128
)

# Purple Circle
circleP = visual.Circle(
    win=mywin,
    autoDraw = False,
    units="pix",
    radius=150,
    fillColor=[1, 0, 1],
    lineColor=[-1, -1, -1],
    edges=128
)

##########################################
# Start screen setup
outlet.push_sample([-1], time.time())
start_text = visual.TextStim(win=mywin, name='start_text',
    text='Press <up> to begin.',
    font='Arial',
    units='norm', pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);
start_press = keyboard.Keyboard()
# keep track of which components have finished
startComponents = [start_text, start_press]

# Finish screen setup
# Initialize components for Routine "finish"
finishClock = core.Clock()
finish_text = visual.TextStim(win=mywin, name='finish_text',
    text='This is the end.\n\nEnd the Marker Streaming now and then press any key to leave.',
    font='Arial',
    units='norm', pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
finish_press = keyboard.Keyboard()



ISI = core.StaticPeriod(screenHz=expInfo['frameRate'])


# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

#########################################
# Start Screen
frameTolerance = 0.001  # how close to onset before 'same' frame
# reset timers
t = 0
_timeToFirstFrame = mywin.getFutureFlipTime(clock="now")
startClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True
while continueRoutine:
    # get current time
    t = startClock.getTime()
    tThisFlip = mywin.getFutureFlipTime(clock=startClock)
    tThisFlipGlobal = mywin.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *start_text* updates
    if start_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_text.frameNStart = frameN  # exact frame index
        start_text.tStart = t  # local t and not account for scr refresh
        start_text.tStartRefresh = tThisFlipGlobal  # on global time
        mywin.timeOnFlip(start_text, 'tStartRefresh')  # time at next scr refresh
        start_text.setAutoDraw(True)
    
    # *start_press* updates
    waitOnFlip = False
    if start_press.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        start_press.frameNStart = frameN  # exact frame index
        start_press.tStart = t  # local t and not account for scr refresh
        start_press.tStartRefresh = tThisFlipGlobal  # on global time
        mywin.timeOnFlip(start_press, 'tStartRefresh')  # time at next scr refresh
        start_press.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        mywin.callOnFlip(start_press.clock.reset)  # t=0 on next screen flip
    if start_press.status == STARTED and not waitOnFlip:
        theseKeys = start_press.getKeys(keyList=['up'], waitRelease=False)
        if len(theseKeys):
            theseKeys = theseKeys[0]  # at least one key was pressed
            
            # check for quit:
            if "escape" == theseKeys:
                endExpNow = True
            start_press.keys = theseKeys.name  # just the last key pressed
            start_press.rt = theseKeys.rt
            # a response ends the routine
            continueRoutine = False
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        mywin.flip()
        
# -------Ending Routine "start"-------
for thisComponent in startComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


##########################################
#For every Trial
##########################################
for ii in range(N): 
    for jj in range(M):
        ISI.start(0.5)  # start a period of 0.5s
        if jj==oddNumList[ii]:
            circleP.draw()
            outlet.push_sample([2], time.time())
        else:
            circleG.draw()
            outlet.push_sample([1], time.time())
        
        ISI.complete() # continue after a 0.5s wait

        if defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        mywin.flip()
        outlet.push_sample([3], time.time())
        core.wait(2)
        mywin.flip()


# ------Prepare to start Routine "finish"-------
routineTimer.add(20.000000)
# update component parameters for each repeat
finish_press.keys = []
finish_press.rt = []
# keep track of which components have finished
finishComponents = [finish_text, finish_press]
for thisComponent in finishComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = mywin.getFutureFlipTime(clock="now")
finishClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1
continueRoutine = True

# -------Run Routine "finish"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = finishClock.getTime()
    tThisFlip = mywin.getFutureFlipTime(clock=finishClock)
    tThisFlipGlobal = mywin.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *finish_text* updates
    if finish_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        finish_text.frameNStart = frameN  # exact frame index
        finish_text.tStart = t  # local t and not account for scr refresh
        finish_text.tStartRefresh = tThisFlipGlobal  # on global time
        mywin.timeOnFlip(finish_text, 'tStartRefresh')  # time at next scr refresh
        finish_text.setAutoDraw(True)
    if finish_text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > finish_text.tStartRefresh + 20-frameTolerance:
            # keep track of stop time/frame for later
            finish_text.tStop = t  # not accounting for scr refresh
            finish_text.frameNStop = frameN  # exact frame index
            mywin.timeOnFlip(finish_text, 'tStopRefresh')  # time at next scr refresh
            finish_text.setAutoDraw(False)
    
    # *finish_press* updates
    waitOnFlip = False
    if finish_press.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        finish_press.frameNStart = frameN  # exact frame index
        finish_press.tStart = t  # local t and not account for scr refresh
        finish_press.tStartRefresh = tThisFlipGlobal  # on global time
        mywin.timeOnFlip(finish_press, 'tStartRefresh')  # time at next scr refresh
        finish_press.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        mywin.callOnFlip(finish_press.clock.reset)  # t=0 on next screen flip
    if finish_press.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > finish_press.tStartRefresh + 20-frameTolerance:
            # keep track of stop time/frame for later
            finish_press.tStop = t  # not accounting for scr refresh
            finish_press.frameNStop = frameN  # exact frame index
            mywin.timeOnFlip(finish_press, 'tStopRefresh')  # time at next scr refresh
            finish_press.status = FINISHED
    if finish_press.status == STARTED and not waitOnFlip:
        theseKeys = finish_press.getKeys(keyList=['y', 'n', 'left', 'right', 'space'], waitRelease=False)
        if len(theseKeys):
            theseKeys = theseKeys[0]  # at least one key was pressed
            
            # check for quit:
            if "escape" == theseKeys:
                endExpNow = True
            finish_press.keys = theseKeys.name  # just the last key pressed
            finish_press.rt = theseKeys.rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in finishComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        mywin.flip()

# -------Ending Routine "finish"-------
for thisComponent in finishComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
mywin.flip()

# these shouldn't be strictly necessary (should auto-save)
# thisExp.saveAsWideText(filename+'.csv')
# thisExp.saveAsPickle(filename)
# logging.flush()

#cleanup
mywin.close()
core.quit()
