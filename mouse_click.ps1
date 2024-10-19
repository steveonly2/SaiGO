# Load necessary assemblies
Add-Type -AssemblyName 'System.Windows.Forms'
Add-Type -AssemblyName 'System.Drawing'

# Define mouse click function using Windows API
Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    public class MouseClicker {
        [DllImport("user32.dll", CharSet = CharSet.Auto, CallingConvention = CallingConvention.StdCall)]
        public static extern void mouse_event(long dwFlags, long dx, long dy, long cButtons, long dwExtraInfo);
        public const int MOUSEEVENTF_LEFTDOWN = 0x02;
        public const int MOUSEEVENTF_LEFTUP = 0x04;
        public static void Click(int x, int y) {
            mouse_event(MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_LEFTUP, x, y, 0, 0);
        }
    }
"@

# Get screen resolution
$screenWidth = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width
$screenHeight = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height

# Calculate adjusted positions based on 1920x1080 reference
$x1 = [math]::Round(794 * ($screenWidth / 1920))
$y1 = [math]::Round(727 * ($screenHeight / 1080))
$x2 = [math]::Round(896 * ($screenWidth / 1920))
$y2 = [math]::Round(448 * ($screenHeight / 1080))
$x3 = [math]::Round(1292 * ($screenWidth / 1920))
$y3 = [math]::Round(725 * ($screenHeight / 1080))

# Move to (794, 727) and click
[System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x1, $y1)
Start-Sleep -Milliseconds 500
[MouseClicker]::Click($x1, $y1)

# Pause before next click
Start-Sleep -Seconds 2

# Move to (896, 448) and click
[System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x2, $y2)
Start-Sleep -Milliseconds 500
[MouseClicker]::Click($x2, $y2)

# Wait for installation to complete
Start-Sleep -Seconds 180  # Adjust based on the installer duration

# Move to (1292, 725) and click
[System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point($x3, $y3)
Start-Sleep -Milliseconds 500
[MouseClicker]::Click($x3, $y3)

# Continue with the installation of Python modules
Start-Sleep -Seconds 5
