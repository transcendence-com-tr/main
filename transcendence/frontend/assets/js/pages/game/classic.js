(function () {

    const keys = {};

    // Klavye olaylarını dinleme
    window.addEventListener("keydown", (event) => {
        keys[event.code] = true;
    });

    window.addEventListener("keyup", (event) => {
        keys[event.code] = false;
    });

    // HTML'deki <canvas> öğesini al
    const canvas = document.getElementById("pongCanvas");

    // Renderer oluştur ve canvas elementine bağla
    const renderer = new THREE.WebGLRenderer({ canvas: canvas });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);

    // Temel Three.js sahnesi
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);

    // Işıklandırma
    const light = new THREE.PointLight(0xffffff, 1, 100);
    light.position.set(0, 10, 10);
    scene.add(light);

    // Zemin
    const floorGeometry = new THREE.PlaneGeometry(20, 10);
    const floorMaterial = new THREE.MeshStandardMaterial({ color: 0x333333 });
    const floor = new THREE.Mesh(floorGeometry, floorMaterial);
    floor.rotation.x = -Math.PI / 2;
    scene.add(floor);

    // Paddles (Raketi)
    const paddleGeometry = new THREE.BoxGeometry(1, 0.2, 2);
    const paddleMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });

    const leftPaddle = new THREE.Mesh(paddleGeometry, paddleMaterial);
    leftPaddle.position.set(-9, 0.1, 0);
    scene.add(leftPaddle);

    const rightPaddle = new THREE.Mesh(paddleGeometry, paddleMaterial);
    rightPaddle.position.set(9, 0.1, 0);
    scene.add(rightPaddle);

    // Top
    const ballGeometry = new THREE.SphereGeometry(0.3, 32, 32);
    const ballMaterial = new THREE.MeshStandardMaterial({ color: 0xff0000 });
    const ball = new THREE.Mesh(ballGeometry, ballMaterial);
    ball.position.set(0, 0.3, 0);
    scene.add(ball);

    // Kamera Pozisyonu
    camera.position.z = 15;
    camera.position.y = 10;
    camera.lookAt(0, 0, 0);

    // Top Hareket Değişkenleri
    let ballVelocity = new THREE.Vector3(0.1, 0, 0.1);

    function update() {
        // Top Hareketi
        ball.position.add(ballVelocity);

        // Duvarlardan Çarpma
        if (ball.position.z >= 5 || ball.position.z <= -5) {
            ballVelocity.z *= -1;
        }

        // Paddle ile Çarpma
        if (ball.position.x <= leftPaddle.position.x + 0.5 &&
            ball.position.z > leftPaddle.position.z - 1 &&
            ball.position.z < leftPaddle.position.z + 1) {
            ballVelocity.x *= -1;
        }

        if (ball.position.x >= rightPaddle.position.x - 0.5 &&
            ball.position.z > rightPaddle.position.z - 1 &&
            ball.position.z < rightPaddle.position.z + 1) {
            ballVelocity.x *= -1;
        }

        // Paddle Kontrolleri
        if (keys["KeyW"] && leftPaddle.position.z < 4.5) leftPaddle.position.z += 0.2;
        if (keys["KeyS"] && leftPaddle.position.z > -4.5) leftPaddle.position.z -= 0.2;
        if (keys["ArrowUp"] && rightPaddle.position.z < 4.5) rightPaddle.position.z += 0.2;
        if (keys["ArrowDown"] && rightPaddle.position.z > -4.5) rightPaddle.position.z -= 0.2;

        // Topun Dışarı Çıkması
        if (ball.position.x <= -10 || ball.position.x >= 10) {
            ball.position.set(0, 0.3, 0); // Reset
            ballVelocity.set((Math.random() > 0.5 ? 0.1 : -0.1), 0, (Math.random() - 0.5) * 0.2);
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        update();
        renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        renderer.render(scene, camera);
    }

    animate();

    document.addEventListener("keyup", function (event) {
        if (event.key === "ArrowUp") {
            upPressed = false;
        } else if (event.key === "ArrowDown") {
            downPressed = false;
        }
    });
})();