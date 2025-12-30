let images = [];
let currentIndex = 0;
const img = document.getElementById('slideshow-image');
const DEFAULT_INTERVAL_MS = 2000; // 8 hours in milliseconds

function shuffleArray(array) {
	for (let i = array.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i + 1));
		[array[i], array[j]] = [array[j], array[i]];
	}
	return array;
}

async function load() {
	try {
		const imagesResponse = await fetch('/api/images');
		images = await imagesResponse.json();
		images = shuffleArray(images);

		const intervalDelay = await fetch('/api/interval');
		const intervalData = await intervalDelay.json();
		const delay = intervalData.delay || DEFAULT_INTERVAL_MS;
		console.log(`Image change interval set to ${delay} ms`);
		if (images.length > 0) {
			showImage();
			setInterval(showImage, delay);
		} else {
			console.error('No images found');
		}
	} catch (error) {
		console.error('Error loading images:', error);
	}
}

function showImage() {
	if (currentIndex % images.length === 0) {
		images = shuffleArray(images);
	}

	img.src = images[currentIndex];
	currentIndex = (currentIndex + 1) % images.length;
}

// Load images and start slideshow
load();