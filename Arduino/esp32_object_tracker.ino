#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

const char* ssid = "ESP32_TEST";
const char* password = "12345678";

#define TRIG_PIN 5
#define ECHO_PIN 18
#define SERVO_PIN 13

WebServer server(80);
Servo myServo;

int servoAngle = 90;
float distance = 0;

float getDistance() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duration == 0) {
    return -1;
  }

  return duration * 0.0343 / 2.0;
}


// =============================
// LIVE DATA
// =============================

void handleData() {

  float d = getDistance();

  String json = "{";
  json += "\"distance\":";
  json += String(d, 1);
  json += ",";
  json += "\"servo\":";
  json += String(servoAngle);
  json += "}";

  server.send(200, "application/json", json);
}


// =============================
// SERVO CONTROL
// =============================

void handleServo() {

  if (!server.hasArg("angle")) {

    server.send(
      400,
      "text/plain",
      "Missing angle"
    );

    return;
  }

  servoAngle = server.arg("angle").toInt();

  servoAngle = constrain(
    servoAngle,
    0,
    180
  );

  myServo.write(servoAngle);

  Serial.print("Servo angle: ");
  Serial.println(servoAngle);

  server.send(
    200,
    "text/plain",
    "Servo moved to " + String(servoAngle)
  );
}


// =============================
// DASHBOARD
// =============================

void handleRoot() {

  String page = R"rawliteral(

<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>ESP32 AI Controller</title>

<style>

body {

  margin: 0;

  font-family: Arial;

  background: #111827;

  color: white;

  text-align: center;

}

.header {

  background: #1f2937;

  padding: 20px;

  font-size: 25px;

  font-weight: bold;

}

.container {

  max-width: 600px;

  margin: auto;

  padding: 15px;

}

.card {

  background: #1f2937;

  border-radius: 15px;

  padding: 20px;

  margin: 15px 0;

}

.value {

  font-size: 40px;

  font-weight: bold;

  margin: 10px;

}

button {

  padding: 15px 25px;

  margin: 5px;

  border: none;

  border-radius: 10px;

  font-size: 17px;

}

.status {

  font-size: 20px;

}

</style>

</head>


<body>


<div class="header">

🤖 AI OBJECT CONTROLLER

</div>


<div class="container">


<div class="card">

<h2>📏 Ultrasonic Distance</h2>

<div id="distance"
class="value">

-- cm

</div>

</div>


<div class="card">

<h2>🦾 Servo Position</h2>

<div id="servo"
class="value">

90°

</div>


<button onclick="moveServo(30)">
LEFT
</button>

<button onclick="moveServo(90)">
CENTER
</button>

<button onclick="moveServo(150)">
RIGHT
</button>

</div>


<div class="card">

<h2>📷 Camera</h2>

<div id="camera"
class="status">

Laptop camera active

</div>

</div>


<div class="card">

<h2>📡 ESP32 Status</h2>

<div class="status">

CONNECTED ✅

</div>

</div>


</div>


<script>


function updateData() {

  fetch("/data")

  .then(response => response.json())

  .then(data => {

    if (data.distance < 0) {

      document.getElementById(
        "distance"
      ).innerHTML = "No object";

    }

    else {

      document.getElementById(
        "distance"
      ).innerHTML =
        data.distance + " cm";

    }

    document.getElementById(
      "servo"
    ).innerHTML =
      data.servo + "°";

  })

  .catch(error => {

    console.log(error);

  });

}


function moveServo(angle) {

  fetch(
    "/servo?angle=" + angle
  )

  .then(response =>
    response.text()
  )

  .then(data => {

    console.log(data);

    updateData();

  });

}


setInterval(
  updateData,
  500
);

updateData();


</script>


</body>

</html>

)rawliteral";


  server.send(
    200,
    "text/html",
    page
  );
}


// =============================
// SETUP
// =============================

void setup() {

  Serial.begin(115200);

  delay(2000);

  pinMode(
    TRIG_PIN,
    OUTPUT
  );

  pinMode(
    ECHO_PIN,
    INPUT
  );


  myServo.attach(
    SERVO_PIN
  );

  myServo.write(90);


  WiFi.mode(WIFI_AP);

  WiFi.softAP(
    ssid,
    password
  );


  Serial.println();

  Serial.println(
    "=============================="
  );

  Serial.println(
    "ESP32 AI CONTROLLER"
  );

  Serial.println(
    "=============================="
  );

  Serial.print(
    "IP: "
  );

  Serial.println(
    WiFi.softAPIP()
  );


  server.on(
    "/",
    handleRoot
  );

  server.on(
    "/data",
    handleData
  );

  server.on(
    "/servo",
    handleServo
  );


  server.begin();


  Serial.println(
    "WEB SERVER STARTED"
  );

}


// =============================
// LOOP
// =============================

void loop() {

  server.handleClient();

}
