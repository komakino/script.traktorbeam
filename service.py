import sys, os, xbmc
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))

from traktorbeam import service, log, addon

if __name__ == '__main__':
    monitor = xbmc.Monitor()

    frequency = addon.getSetting("frequency")
    seconds = float(frequency) * 60 * 60

    log.info("Starting service. Running every %s seconds" % seconds)

    while True:

        service.run()

        # Sleep/wait for abort
        if monitor.waitForAbort(seconds):
            # Abort was requested while waiting. We should exit
            log.info("Stopping service")
            break
