import picarx_improved
import atexit


if __name__ == "__main__":
    px = picarx_improved.Picarx()
    px.maneuver_follow_line()
    atexit.register(px.stop)
