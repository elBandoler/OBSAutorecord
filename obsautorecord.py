import obspython as obs
import math, time

# Description displayed in the Scripts dialog window
def script_description():
  return """Autorecord!
  Automatically start recording at a certain time, and end at another set time.
  Define times below."""

# Start recording if not recording
def start_recording():
    print("start_recording:")
    print(obs.obs_frontend_recording_active())
    if not obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_start()

# Stop recording if recording
def stop_recording():
    print("stop_recording:")
    print(obs.obs_frontend_recording_active())
    if obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()

# Called to set default values of data settings
def script_defaults(settings):
    obs.obs_data_set_default_int(settings, "start_hour", 0)
    obs.obs_data_set_default_int(settings, "start_minute", 0)
    obs.obs_data_set_default_int(settings, "start_second", 0)
    obs.obs_data_set_default_bool(settings, "start_enabled", False)
    obs.obs_data_set_default_int(settings, "stop_hour", 0)
    obs.obs_data_set_default_int(settings, "stop_minute", 0)
    obs.obs_data_set_default_int(settings, "stop_second", 0)
    obs.obs_data_set_default_bool(settings, "stop_enabled", False)

# Called to display the properties GUI
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_int_slider(props, "start_hour", "Start Recording Hour", 0, 23, 1)
    obs.obs_properties_add_int_slider(props, "start_minute", "Start Recording Minute", 0, 59, 1)
    obs.obs_properties_add_int_slider(props, "start_second", "Start Recording Second", 0, 59, 1)
    obs.obs_properties_add_bool(props, "start_enabled", "Enable Autostart")
    obs.obs_properties_add_int_slider(props, "stop_hour", "Stop Recording Hour", 0, 23, 1)
    obs.obs_properties_add_int_slider(props, "stop_minute", "Stop Recording Minute", 0, 59, 1)
    obs.obs_properties_add_int_slider(props, "stop_second", "Stop Recording Second", 0, 59, 1)
    obs.obs_properties_add_bool(props, "stop_enabled", "Enable Autostop")
    return props

# Called after change of settings including once after script load
def script_update(settings):
    global start_hour, start_minute, start_second, start_enabled, stop_hour, stop_minute, stop_second, stop_enabled
    start_hour = obs.obs_data_get_int(settings, "start_hour")
    start_minute = obs.obs_data_get_int(settings, "start_minute")
    start_second = obs.obs_data_get_int(settings, "start_second")
    start_enabled = obs.obs_data_get_bool(settings, "start_enabled")
    stop_hour = obs.obs_data_get_int(settings, "stop_hour")
    stop_minute = obs.obs_data_get_int(settings, "stop_minute")
    stop_second = obs.obs_data_get_int(settings, "stop_second")
    stop_enabled = obs.obs_data_get_bool(settings, "stop_enabled")

# Called at script unload
def script_unload():
    stop_recording()
    obs.timer_remove(time_elapsed)

# Runs every 1ms, timer
def time_elapsed():
    seconds = time.time()
    local_time = time.localtime(seconds)
    if start_enabled and local_time.tm_hour == start_hour and local_time.tm_min == start_minute and local_time.tm_sec == start_second:
        start_recording()
    elif stop_enabled and local_time.tm_hour == stop_hour and local_time.tm_min == stop_minute and local_time.tm_sec == stop_second and stop_enabled:
        stop_recording()
    
obs.timer_add(time_elapsed, 1000)