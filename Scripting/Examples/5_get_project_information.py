#!/usr/bin/env python

"""
Example DaVinci Resolve script:
Display project information: timeline, clips within timelines and media pool structure.
Example usage: 5_get_project_information.py
"""

from python_get_resolve import GetResolve

def DisplayTimelineTrack( timeline, trackType, displayShift ):
    trackCount = timeline.GetTrackCount(trackType)
    for index in range (1, int(trackCount) + 1):
        print(displayShift + "- " + trackType + " " + str(index))
        clips = timeline.GetItemListInTrack(trackType, index)
        for clip in clips:
            print(displayShift + "    " + clip.GetName())
    return

def DisplayTimelineInfo( timeline, displayShift ):
    print(displayShift + "- " + timeline.GetName())
    displayShift = "  " + displayShift
    DisplayTimelineTrack(timeline , "video", displayShift)
    DisplayTimelineTrack(timeline , "audio", displayShift)
    DisplayTimelineTrack(timeline , "subtitle", displayShift)
    return

def DisplayTimelinesInfo( project ):
    print("- Timelines")
    timelineCount = project.GetTimelineCount()

    for index in range (0, int(timelineCount)):
        DisplayTimelineInfo(project.GetTimelineByIndex(index + 1), "  ")
    return

def DisplayFolderInfo( folder, displayShift ):
    print(displayShift + "- " + folder.GetName())
    clips = folder.GetClipList()
    for clip in clips:
        print(displayShift + "  " + clip.GetClipProperty("File Name"))

    displayShift = "  " + displayShift

    folders = folder.GetSubFolderList()
    for folder in folders:
        DisplayFolderInfo(folder, displayShift)
    return

def DisplayMediaPoolInfo( project ):
    mediaPool = project.GetMediaPool()
    print("- Media pool")
    DisplayFolderInfo(mediaPool.GetRootFolder(), "  ")
    return

def DisplayProjectInfo( project ):
    print("-----------")
    print("Project '" + project.GetName() +"':")
    print("  Framerate " + str(project.GetSetting("timelineFrameRate")))
    print("  Resolution " + project.GetSetting("timelineResolutionWidth") + "x" + project.GetSetting("timelineResolutionHeight"))

    DisplayTimelinesInfo(project)
    print("")
    DisplayMediaPoolInfo(project)
    return

# Get currently open project
resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()

DisplayProjectInfo(project)
