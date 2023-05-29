import sys
import time
import DaVinciResolveScript as bmd

def GetResolve():
    try:
        resolve = bmd.scriptapp("Resolve")
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath = os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
        elif sys.platform.startswith("linux"):
            expectedPath = "/opt/resolve/libs/Fusion/Modules/"

        print("Unable to find module DaVinciResolveScript from $PYTHONPATH - trying default locations")
        try:
            resolve = bmd.scriptapp(expectedPath)
        except ImportError:
            print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
            print("For a default DaVinci Resolve installation, the module is expected to be located in: " + expectedPath)
            sys.exit()

    return resolve

def AddTimelineToRender(project, timeline, presetName, targetDirectory, renderFormat, renderCodec):
    project.SetCurrentTimeline(timeline)
    project.LoadRenderPreset(presetName)
    project.SetCurrentRenderFormatAndCodec(renderFormat, renderCodec)
    project.SetRenderSettings({"SelectAllFrames": 1, "TargetDir": targetDirectory})
    return project.AddRenderJob()

def RenderAllTimelines(resolve, presetName, targetDirectory, renderFormat, renderCodec):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    renderJobManager = project.GetRenderJobManager()

    for timelineIndex in range(1, project.GetTimelineCount() + 1):
        timeline = project.GetTimelineByIndex(timelineIndex)
        if not AddTimelineToRender(project, timeline, presetName, targetDirectory, renderFormat, renderCodec):
            return False

    renderJobManager.StartRendering()

    return True

def IsRenderingInProgress(resolve):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False

    return project.IsRenderingInProgress()

def WaitForRenderingCompletion(resolve):
    while IsRenderingInProgress(resolve):
        time.sleep(1)

def ApplyDRXToAllTimelineClips(timeline, path, gradeMode=0):
    trackCount = timeline.GetTrackCount("video")

    for index in range(1, int(trackCount) + 1):
        clips = timeline.GetItemListInTrack("video", index)
        if not timeline.ApplyGradeFromDRX(path, int(gradeMode), clips):
            return False

    return True

def ApplyDRXToAllTimelines(resolve, path, gradeMode=0):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        return False
    timelineCount = project.GetTimelineCount()

    for index in range(0, int(timelineCount)):
        timeline = project.GetTimelineByIndex(index + 1)
        project.SetCurrentTimeline(timeline)
        if not ApplyDRXToAllTimelineClips(timeline, path, gradeMode):
            return False

    return True

def DeleteAllRenderJobs(resolve):
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    renderJobManager = project.GetRenderJobManager()
    renderJobManager.DeleteAllRenderJobs()

# Predefined inputs:
projectName = "MyProject2334"
mediaPath = "F:\\media\\The_Office_S03\\OCF\\D01_02082022\\CAM_A_XOCN\\A001CJ90\\A001CJ90\\Clip\\A001C001_180705TE"
exportLocation = "F:\\output"
presetName = "Custom"
renderFormat = "DNxHR SQ"
renderCodec = "DNxHR SQ"
lutPath = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT\DJI\DJI_Phantom4_DLOG2Rec709.cube"
drxPath = "F:\JV_skrypty\DRX_test_1.1.1.drx"
gradeMode = 0

# Create project and set parameters:
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.CreateProject(projectName)

if not project:
    print("Unable to create a project '" + projectName + "'")
    sys.exit()

# Set project settings:
project.SetSetting("timelineFrameRate", "25")
project.SetSetting("timelineResolutionWidth", "1920")
project.SetSetting("timelineResolutionHeight", "1080")

# Add folder contents to Media Pool:
mediapool = project.GetMediaPool()
rootFolder = mediapool.GetRootFolder()

# Import video clips:
mediaStorage = resolve.GetMediaStorage()
clips = mediaStorage.AddItemsToMediaPool(mediaPath)

if clips == -1:
    print("Failed to add clips to Media Pool")
    sys.exit()
elif clips == 0:
    print("No clips found in the specified media path")
    sys.exit()

# Sort clips by name:
clips = sorted(clips, key=lambda clip: clip.GetClipProperty("File Name")) if isinstance(clips, list) else [clips]

# Create timeline:
timelineName = "Timeline 1"
timeline = mediapool.CreateEmptyTimeline(timelineName)

if not timeline:
    print("Unable to create timeline '" + timelineName + "'")
    sys.exit()

# Append clips to the timeline:
for clip in clips:
    mediapool.AppendToTimeline(clip)

# Apply LUT to clips:
#lutFilter = timeline.AddVideoFilter("Color")
#lutFilter.SetPluginData("InputLUT", lutPath)

# Apply DRX to all timelines:
if not ApplyDRXToAllTimelines(resolve, drxPath, gradeMode):
    print("Unable to apply DRX to all timelines")
    sys.exit()

# Wait for rendering completion if there is any ongoing rendering:
WaitForRenderingCompletion(resolve)

# Add timelines to render:
if not RenderAllTimelines(resolve, presetName, exportLocation, renderFormat, renderCodec):
    print("Failed to add timelines to render")
    sys.exit()

# Wait for rendering completion:
WaitForRenderingCompletion(resolve)

# Delete all render jobs:
DeleteAllRenderJobs(resolve)

print("Project created and clips imported successfully. Rendering started.")
