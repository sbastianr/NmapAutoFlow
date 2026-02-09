import flet as ft
import inspect

print(f"Flet version: {ft.version}")

try:
    print(f"ft.app exists: {hasattr(ft, 'app')}")
    print(f"ft.run exists: {hasattr(ft, 'run')}")
except:
    pass

try:
    print(f"Icons starting with WIFI:")
    for name in dir(ft.icons):
        if "WIFI" in name:
            print(name)
except:
    print("Could not list icons")

try:
    print(f"ElevatedButton exists: {hasattr(ft, 'ElevatedButton')}")
    print(f"Button exists: {hasattr(ft, 'Button')}")
    print(f"FilledButton exists: {hasattr(ft, 'FilledButton')}")
except:
    pass
