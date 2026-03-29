import { useState, useEffect } from "react";
import Uploady, {
  useBatchFinishListener,
  useBatchStartListener,
} from "@rpldy/uploady";
import { asUploadButton } from "@rpldy/upload-button";
import * as S from "./App.styles";

type Image = {
  name: string;
  url: string;
};

function App() {
  const [refreshInterval, setRefreshInterval] = useState("8");
  const [timeUnit, setTimeUnit] = useState("hours");
  const [colorTemp, setColorTemp] = useState("");
  const [images, setImages] = useState<Image[]>([]);
  const [uploadBatchCount, setUploadBatchCount] = useState(0);

  // backend url is hosted on port 7100 of the same hostname as the frontend
  const baseUrl = `http://${window.location.hostname}:7100`;
  const uploadUrl = `${baseUrl}/api/upload`;

  const updateConfig = (
    refreshInterval: string,
    timeUnit: string,
    colorTemp: string,
  ) => {
    console.log("Updating config:", {
      refreshInterval,
      timeUnit,
      colorTemp,
    });
    // Update config via API
    fetch(`${baseUrl}/api/config`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refreshInterval,
        timeUnit,
        colorTemp,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Config updated successfully:", data);
      })
      .catch((error) => {
        console.error("Error updating config:", error);
      });
  };

  const deleteImage = (imageName: string) => {
    console.log("Deleting image:", imageName);
    fetch(`${baseUrl}/api/delete_image`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name: imageName }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        // Remove deleted image from state
        setImages((prevImages) =>
          prevImages.filter((img) => img.name !== imageName),
        );
      })
      .catch((error) => {
        console.error("Error deleting image:", error);
      });
  };

  useEffect(() => {
    console.log(`Fetching config from ${baseUrl}/api/config`);
    // Fetch config from API
    fetch(`${baseUrl}/api/config`)
      .then((response) => response.json())
      .then((data) => {
        setRefreshInterval(data.refreshInterval || "8");
        setTimeUnit(data.timeUnit || "hours");
        setColorTemp(data.colorTemp || "");
      })
      .catch((error) => {
        console.error("Error fetching config:", error);
        setRefreshInterval("8");
        setTimeUnit("hours");
        setColorTemp("");
      });
  }, []);

  useEffect(() => {
    console.log(`Fetching images from ${baseUrl}/api/images`);
    fetch(`${baseUrl}/api/images`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Images fetched:", data);
        setImages(data);
      })
      .catch((error) => {
        console.error("Error fetching images:", error);
      });
  }, []);

  const UploadCompletionListener = () => {
    useBatchFinishListener(() => {
      setUploadBatchCount((count) => count - 1);

      // If the last batch has finished uploading, refetch the images
      if (uploadBatchCount <= 1) {
        fetch(`${baseUrl}/api/images`)
          .then((response) => response.json())
          .then((data) => {
            console.log("Updated images fetched:", data);
            setImages(data);
          })
          .catch((error) => {
            console.error("Error fetching updated images:", error);
          });
      }
    });

    useBatchStartListener(() => {
      setUploadBatchCount((count) => count + 1);
    });
    return null;
  };

  const UploadButton = asUploadButton(
    (props: React.ComponentProps<"button">) => {
      return uploadBatchCount === 0 ? (
        <S.StyledUploadButton {...props}>Upload Images</S.StyledUploadButton>
      ) : null;
    },
  );

  return (
    <S.AppContainer>
      <S.Header>
        <S.HeaderTitle>Pi-Frame Configuration</S.HeaderTitle>
      </S.Header>

      <S.Content>
        <S.Label>
          <span>Refresh Interval:</span>
          <S.InputGroup>
            <S.NumberInput
              type="number"
              id="refreshInterval"
              name="refreshInterval"
              value={refreshInterval}
              onChange={(e) => {
                setRefreshInterval(e.target.value);
                updateConfig(e.target.value, timeUnit, colorTemp);
              }}
            />
            <S.Select
              id="timeUnit"
              name="timeUnit"
              value={timeUnit}
              onChange={(e) => {
                setTimeUnit(e.target.value);
                updateConfig(refreshInterval, e.target.value, colorTemp);
              }}
            >
              <option value="hours">hours</option>
              <option value="minutes">minutes</option>
            </S.Select>
          </S.InputGroup>
        </S.Label>
        <S.Label>
          <span>Color Temperature (K):</span>
          <S.InputGroup>
            <S.WideNumberInput
              type="number"
              id="colorTemp"
              name="colorTemp"
              placeholder="1000 - 10,000"
              value={colorTemp}
              onChange={(e) => {
                console.log("Color Temp changed to:", e.target.value);
                setColorTemp(e.target.value);
                updateConfig(refreshInterval, timeUnit, e.target.value);
              }}
            />
          </S.InputGroup>
        </S.Label>
        <S.Subtitle>
          Leave empty to use the display's default setting.
        </S.Subtitle>

        <S.ImagesSection>
          <Uploady
            accept="image/jpeg,image/png,image/gif"
            destination={{ url: uploadUrl }}
          >
            <UploadCompletionListener />
            <UploadButton />
          </Uploady>

          {images.map((image) => (
            <S.ImageListItem key={image.name}>
              <S.ImageThumbnail
                src={`${baseUrl}${image.url}`}
                alt={image.name}
              />
              <S.ImageName>{image.name}</S.ImageName>
              <div style={{ flexGrow: 1 }} />
              <S.DeleteButton
                onClick={() => {
                  deleteImage(image.name);
                }}
              >
                ✕
              </S.DeleteButton>
            </S.ImageListItem>
          ))}
        </S.ImagesSection>
      </S.Content>
    </S.AppContainer>
  );
}

export default App;
