import { useState, useEffect } from "react";
import Uploady, {
  useBatchFinishListener,
  useBatchStartListener,
} from "@rpldy/uploady";
import { asUploadButton } from "@rpldy/upload-button";
import * as S from "./App.styles";
import "react-datetime-picker/dist/DateTimePicker.css";
import "react-calendar/dist/Calendar.css";
import "react-clock/dist/Clock.css";

type Image = {
  name: string;
  url: string;
};

const UploadButton = asUploadButton((props: React.ComponentProps<"button">) => {
  return <S.StyledUploadButton {...props}>Upload Images</S.StyledUploadButton>;
});

const DEFAULT_COLOR_TEMP_OVERRIDE = "5000";
const DEFAULT_NIGHT_MODE_START = "20";
const DEFAULT_NIGHT_MODE_END = "7";
const DEFAULT_REFRESH_INTERVAL = "8";
const DEFAULT_REFRESH_UNIT = "hours";

function UploadCompletionListener({
  baseUrl,
  setImages,
  setIsUploading,
}: {
  baseUrl: string;
  setImages: React.Dispatch<React.SetStateAction<Image[]>>;
  setIsUploading: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  useBatchStartListener(() => {
    setIsUploading(true);
  });

  useBatchFinishListener(() => {
    Promise.all([
      fetch(`${baseUrl}/api/images`).then((response) => response.json()),
      new Promise((resolve) => setTimeout(resolve, 3000)),
    ])
      .then(([data]) => {
        console.log("Updated images fetched:", data);
        setImages(data as Image[]);
        setIsUploading(false);
      })
      .catch((error) => {
        console.error("Error fetching updated images:", error);
        setIsUploading(false);
      });
  });

  return null;
}

function App() {
  const [refreshInterval, setRefreshInterval] = useState(
    DEFAULT_REFRESH_INTERVAL,
  );
  const [timeUnit, setTimeUnit] = useState(DEFAULT_REFRESH_UNIT);
  const [colorTempOverride, setColorTempOverride] = useState(false);
  const [colorTemp, setColorTemp] = useState("");
  const [images, setImages] = useState<Image[]>([]);
  const [enableNightMode, setEnableNightMode] = useState(false);
  const [nightModeStart, setNightModeStart] = useState(
    DEFAULT_NIGHT_MODE_START,
  );
  const [nightModeEnd, setNightModeEnd] = useState(DEFAULT_NIGHT_MODE_END);
  // backend url is hosted on port 50001 of the same hostname as the frontend
  const baseUrl = `http://${window.location.hostname}:50001`;
  const uploadUrl = `${baseUrl}/api/upload`;

  const [isUploading, setIsLoading] = useState(false);
  const [systemDate, setSystemDate] = useState<Date | null>(null);

  const updateConfig = (
    updates: Partial<{
      refreshInterval: string;
      timeUnit: string;
      colorTemp: string;
      nightModeStart: string;
      nightModeEnd: string;
    }> = {},
  ) => {
    const config = {
      refreshInterval,
      timeUnit,
      colorTemp,
      nightModeStart,
      nightModeEnd,
      ...updates,
    };
    console.log("Updating config:", config);
    // Update config via API
    fetch(`${baseUrl}/api/config`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
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
    fetch(`${baseUrl}/api/date`)
      .then((response) => response.json())
      .then((data) => {
        if (data.date) {
          setSystemDate(new Date(data.date));
        }
      })
      .catch((error) => {
        console.error("Error fetching system date:", error);
      });
  }, []);

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

  return (
    <S.AppContainer>
      <S.Header>
        <S.HeaderTitle>Pi-Frame Configuration</S.HeaderTitle>
      </S.Header>

      <S.Content>
        <S.Label>
          <span>Refresh Interval:</span>
          <S.InputGroupX>
            <S.NumberInput
              type="number"
              id="refreshInterval"
              name="refreshInterval"
              value={refreshInterval}
              onChange={(e) => {
                setRefreshInterval(e.target.value);
                updateConfig({ refreshInterval: e.target.value });
              }}
            />
            <S.Select
              id="timeUnit"
              name="timeUnit"
              value={timeUnit}
              onChange={(e) => {
                setTimeUnit(e.target.value);
                updateConfig({ timeUnit: e.target.value });
              }}
            >
              <option value="hours">hours</option>
              <option value="minutes">minutes</option>
            </S.Select>
          </S.InputGroupX>
        </S.Label>
        <S.Label>
          <S.InputGroupY>
            <S.InputGroupX>
              <span>Night Mode:</span>
              <S.CheckboxInput
                type="checkbox"
                id="nightMode"
                name="nightMode"
                checked={enableNightMode}
                onChange={(e) => {
                  setEnableNightMode(e.target.checked);
                  setNightModeStart(
                    e.target.checked ? DEFAULT_NIGHT_MODE_START : "",
                  );
                  setNightModeEnd(
                    e.target.checked ? DEFAULT_NIGHT_MODE_END : "",
                  );
                }}
              />
            </S.InputGroupX>
            {enableNightMode ? (
              <>
                <S.InputGroupX>
                  <span>Night mode start (hour, 0-23):</span>
                  <S.NumberInput
                    type="number"
                    id="nightStart"
                    name="nightStart"
                    value={nightModeStart}
                    onChange={(e) => {
                      setNightModeStart(e.target.value);
                      updateConfig({ nightModeStart: e.target.value });
                    }}
                  />
                </S.InputGroupX>
                <S.InputGroupX>
                  <span>Night mode end (hour, 0-23):</span>
                  <S.NumberInput
                    type="number"
                    id="nightEnd"
                    name="nightEnd"
                    value={nightModeEnd}
                    onChange={(e) => {
                      setNightModeEnd(e.target.value);
                      updateConfig({ nightModeEnd: e.target.value });
                    }}
                  />
                </S.InputGroupX>
              </>
            ) : null}
          </S.InputGroupY>
        </S.Label>
        <S.Label>
          <span>System date:</span>
          <S.DatePicker
            value={systemDate}
            onChange={(value) => {
              setSystemDate(value);
              if (value) {
                const iso = value.toISOString().slice(0, 19);
                fetch(`${baseUrl}/api/date`, {
                  method: "PUT",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ date: iso }),
                }).catch((error) => {
                  console.error("Error updating system date:", error);
                });
              }
            }}
          />
        </S.Label>
        <S.Label>
          <S.InputGroupY>
            <S.InputGroupX>
              <span>Color Temperature Override:</span>
              <S.CheckboxInput
                type="checkbox"
                id="colorOverride"
                name="colorOverride"
                checked={colorTempOverride}
                onChange={(e) => {
                  setColorTempOverride(e.target.checked);
                  const newTemp = e.target.checked
                    ? DEFAULT_COLOR_TEMP_OVERRIDE
                    : "";
                  setColorTemp(newTemp);
                  updateConfig({ colorTemp: newTemp });
                }}
              />
            </S.InputGroupX>
            {colorTempOverride ? (
              <S.InputGroupX>
                <span>{colorTemp}K</span>
                <S.SliderInput
                  type="range"
                  min={1000}
                  max={10000}
                  id="colorTemp"
                  name="colorTemp"
                  value={colorTemp}
                  onChange={(e) => {
                    console.log("Color Temp changed to:", e.target.value);
                    setColorTemp(e.target.value);
                    updateConfig({ colorTemp: e.target.value });
                  }}
                />
              </S.InputGroupX>
            ) : null}
          </S.InputGroupY>
        </S.Label>

        <S.Section>
          <Uploady
            accept="image/jpeg,image/png,image/gif"
            destination={{ url: uploadUrl }}
          >
            <UploadCompletionListener
              baseUrl={baseUrl}
              setImages={setImages}
              setIsUploading={setIsLoading}
            />
            {isUploading && (
              <S.UploadingCell>
                <S.Spinner />
                Uploading...
              </S.UploadingCell>
            )}
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
        </S.Section>
      </S.Content>
    </S.AppContainer>
  );
}

export default App;
