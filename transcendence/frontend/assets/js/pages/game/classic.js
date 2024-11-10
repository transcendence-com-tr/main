(function () {
    const canvas = document.getElementById("pongCanvas");
    const context = canvas.getContext("2d");

    const ballRadius = 5;
    let x = canvas.width / 2;
    let y = canvas.height / 2;
    let dx = 2;
    let dy = 2;

    const paddleWidth = 10;
    const paddleHeight = 50;
    let paddleY = (canvas.height - paddleHeight) / 2;
    let rightPaddleY = (canvas.height - paddleHeight) / 2;

    let upPressed = false;
    let downPressed = false;

// Oyun döngüsü
    function draw() {
        context.clearRect(0, 0, canvas.width, canvas.height);

        // Topu çiz
        context.beginPath();
        context.arc(x, y, ballRadius, 0, Math.PI * 2);
        context.fillStyle = "rgba(255, 128, 210, 0.7)"
        context.fill();
        context.closePath();

        // Sol paddle'ı çiz
        context.fillStyle = "#ff4d4d";
        context.fillRect(0, paddleY, paddleWidth, paddleHeight);

        context.fillStyle = "#15d8fd";
        context.fillRect(canvas.width - paddleWidth, rightPaddleY, paddleWidth, paddleHeight);

        // Topun hareketi
        x += dx;
        y += dy;

        // Topun duvarlara çarpması
        if (y + dy > canvas.height - ballRadius || y + dy < ballRadius) {
            dy = -dy;
        }

        // Topun paddle'lara çarpması
        if (x + dx < paddleWidth) {
            if (y > paddleY && y < paddleY + paddleHeight) {
                dx = -dx;
            } else {
                // Sağ paddle'a gol
                resetBall();
            }
        } else if (x + dx > canvas.width - ballRadius - paddleWidth) {
            if (y > rightPaddleY && y < rightPaddleY + paddleHeight) {
                dx = -dx;
            } else {
                // Sol paddle'a gol
                resetBall();
            }
        }

        // Paddle'ı hareket ettir
        if (upPressed && rightPaddleY > 0) {
            rightPaddleY -= 1;
        } else if (downPressed && rightPaddleY < canvas.height - paddleHeight) {
            rightPaddleY += 1;
        }

        requestAnimationFrame(draw);
    }

// Topun konumunu sıfırla
    function resetBall() {
        x = canvas.width / 2;
        y = canvas.height / 2;
        dx = -dx;
    }

// Klavye olaylarını dinle
    document.addEventListener("keydown", function (event) {
        if (event.key === "ArrowUp" || event.key === "ArrowDown")
            event.preventDefault();
        if (event.key === "ArrowUp") {
            upPressed = true;
        } else if (event.key === "ArrowDown") {
            downPressed = true;
        }
    });

    document.addEventListener("keyup", function (event) {
        if (event.key === "ArrowUp") {
            upPressed = false;
        } else if (event.key === "ArrowDown") {
            downPressed = false;
        }
    });


    draw();

})();