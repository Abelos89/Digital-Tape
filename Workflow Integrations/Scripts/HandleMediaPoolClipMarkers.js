/**
 * Sample script to demonstrate following operations to first MediaPool clip in DaVinci Resolve Studio:
 * 1. Add markers
 * 2. Get markers
 * 3. Set customData
 * 4. Delete markers
 *
 * NOTE: Add one clip (recommended clip duration >= 80 frames) in the MediaPool root bin before running this script.
 */

const WorkflowIntegration = require('./WorkflowIntegration.node');

// Configurable variables
PLUGIN_ID = "com.blackmagicdesign.resolve.sampleplugin"; // update it to your unique plugin Id as mentioned in the manifest.xml file

// Main function to perform all actions
function main(pluginId) {
    // Check pluginId
    if (!pluginId) {
        alert("Error: 'pluginId' is empty, update it to some valid value and try again!");
        return false;
    }

    // Initialize
    isInitialized = WorkflowIntegration.Initialize(pluginId);
    if (!isInitialized) {
        alert("Error: Failed to initialize!");
        return;
    }

    // Get resolve object
    resolve = WorkflowIntegration.GetResolve();
    if (!resolve) {
        alert("Error: Failed to get resolve object!");
        return;
    }

    // Open Media page
    resolve.OpenPage("media");

    // Get supporting objects
    projectManager = resolve.GetProjectManager();
    project = projectManager.GetCurrentProject();
    mediaPool = project.GetMediaPool();
    rootBin = mediaPool.GetRootFolder();

    // Go to root bin
    mediaPool.SetCurrentFolder(rootBin);

    // Gets clips
    clips = rootBin.GetClipList();
    if (!clips || !clips[0]) {
        alert("Error: MediaPool root bin doesn't contain any clips, add one clip (recommended clip duration >= 80 frames) and try again!");
        return;
    }

    // Choose first clip in the list
    clip = clips[0];

    // Get clip frames
    framesProperty = clip.GetClipProperty("Frames");
    if (!framesProperty) {
        alert("Error: Failed to get clip 'Frames' property !");
        return;
    }
    numFrames = parseInt(framesProperty);

    // Add Markers
    if (numFrames >= 1) {
        isSuccess = clip.AddMarker(/*markerPos*/ 1, /*color*/ "Red", /*markerName*/ "Marker1", /*note*/ "Marker1 at frame 1", /*duration*/ 1);
        if (isSuccess) {
            console.log("Added marker at FrameId:1");
        }
    }

    if (numFrames >= 20) {
        isSuccess = clip.AddMarker(/*markerPos*/ 20, /*color*/ "Blue", /*markerName*/ "Marker2", /*note*/ "Marker2 at frame 20", /*duration*/ 1, /*customData*/ "My Custom Data"); // marker with custom data
        if (isSuccess) {
            console.log("Added marker at FrameId:20");
        }
    }

    if (numFrames >= (50 + 20)) {
        isSuccess = clip.AddMarker(/*markerPos*/ 50, /*color*/ "Green", /*markerName*/ "Marker3", /*note*/ "Marker3 at frame 50 (duration 20)", /*duration*/ 20); // marker with duration 20 frames
        if (isSuccess) {
            console.log("Added marker at FrameId:50");
        }
    }

    // Get all markers for the clip
    markers = clip.GetMarkers();
    for (let [frameId, markerInfo] of Object.entries(markers)) {
        console.log("Marker at FrameId:" + frameId);
        console.log(markerInfo);
    }

    // Get marker using custom data
    markerWithCustomData = clip.GetMarkerByCustomData("My Custom Data");
    console.log("Marker with customData:");
    console.log(markerWithCustomData);

    // Set marker custom data
    updatedCustomData = "Updated Custom Data";
    isSuccess = clip.UpdateMarkerCustomData(20, updatedCustomData);
    if (isSuccess) {
        console.log("Updated marker customData at FrameId:20");
    }

    // Get marker custom data
    customData = clip.GetMarkerCustomData(20);
    console.log(`Marker CustomData at FrameId:20 is:'${customData}'`);

    // Delete marker using color
    isSuccess = clip.DeleteMarkersByColor("Red");
    if (isSuccess) {
        console.log("Deleted marker with color:'Red'");
    }

    // Delete marker using frame number
    isSuccess = clip.DeleteMarkerAtFrame(50)
    if (isSuccess) {
        console.log("Deleted marker at frameNum:50");
    }

    // Delete marker using custom data
    isSuccess = clip.DeleteMarkerByCustomData(updatedCustomData)
    if (isSuccess) {
        console.log(`Deleted marker with customData:'${updatedCustomData}'`);
    }

    // Done
    // WorkflowIntegration.CleanUp(); // Call CleanUp() during plugin app quit only
}

// Run main function
main(PLUGIN_ID);
