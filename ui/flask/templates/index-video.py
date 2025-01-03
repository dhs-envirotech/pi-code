<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Motor Control with Video Feed</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            background-color: #e6f7ff;
        }
        #joystick-container {
            position: relative;
            width: 200px;
            height: 200px;
            margin: 20px auto;
            border: 1px solid #000;
        }
        #joystick {
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 50%;
            background: blue;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        header, footer {
            padding: 20px;
            text-align: center;
            background-color: #007bff;
            color: white;
        }
        .video-feed {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            border: 2px solid #000;
            border-radius: 5px;
            overflow: hidden;
        }
    </style>
</head>
<body>

    <header>
        <h1>Raspberry Pi Motor Control</h1>
    </header>

    <div class="container">
        <div class="row">
            <div class="col text-center">
                <h3>Live Video Feed</h3>
                <div class="video-feed">
                    <img src="{{ url_for('video_feed') }}" class="img-fluid" alt="Video Feed">
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col text-center">
                <h3>Joystick Control</h3>
                <div id="joystick-container">
                    <div id="joystick"></div>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>© 2024 Raspberry Pi Motor Controller</p>
    </footer>

    <!-- Include Nipple.js for the virtual joystick -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/nipplejs/0.10.1/nipplejs.min.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var joystickContainer = document.getElementById('joystick-container');
            var joystick = nipplejs.create({
                zone: joystickContainer,
                mode: 'static',
                position: { top: '50%', left: '50%' },
                color: 'blue'
            });

            joystick.on('move', function (evt, data) {
                if (data.angle && data.force) {
                    // Send joystick data to the server (Flask)
                    var xhr = new XMLHttpRequest();
                    xhr.open('POST', '/control');
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    xhr.send(JSON.stringify({ angle: data.angle.degree, force: data.force }));
                }
            });

            joystick.on('end', function () {
                // Stop the motor when the joystick is released
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/stop');
                xhr.send();
            });
        });
    </script>

    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>

