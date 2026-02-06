# singletons/test_logger.py

from logger_singleton import LoggerSingleton  # Import your singleton class

# -------------------------------
# Get two logger instances
# -------------------------------
logger1 = LoggerSingleton().get_logger()
logger2 = LoggerSingleton().get_logger()

# -------------------------------
# Test singleton behavior
# -------------------------------
assert logger1 is logger2, "LoggerSingleton failed: multiple instances exist!"
print("Singleton test passed ✅ Both instances are the same")

# -------------------------------
# Test logging messages
# -------------------------------
logger1.info("INFO: This is an info message from logger1")
logger1.warning("WARNING: This is a warning message from logger1")
logger2.error("ERROR: This is an error message from logger2 (same logger as logger1)")

print("Logger output test completed successfully ✅")
