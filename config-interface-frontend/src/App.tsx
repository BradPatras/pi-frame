import { useState, useEffect } from "react";
import Uploady, { useItemProgressListener } from "@rpldy/uploady";
import { asUploadButton } from "@rpldy/upload-button";
import * as S from "./App.styles";

function App() {
  const [refreshInterval, setRefreshInterval] = useState("8");
  const [timeUnit, setTimeUnit] = useState("hours");
  const [colorTemp, setColorTemp] = useState("");

  useEffect(() => {
    // Fetch config from API
    fetch("/api/config")
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

  const LogProgress = () => {
    useItemProgressListener((item) => {
      console.log(
        `>>>>> (hook) File ${item.file.name} completed: ${item.completed}`,
      );
    });
    return null;
  };

  const UploadButton = asUploadButton(
    (props: React.ComponentProps<"button">) => {
      return (
        <S.StyledUploadButton {...props}>Upload Images</S.StyledUploadButton>
      );
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
              onChange={(e) => setRefreshInterval(e.target.value)}
            />
            <S.Select
              id="timeUnit"
              name="timeUnit"
              value={timeUnit}
              onChange={(e) => setTimeUnit(e.target.value)}
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
              onChange={(e) => setColorTemp(e.target.value)}
            />
          </S.InputGroup>
        </S.Label>

        <S.UploadSection>
          <Uploady destination={{ url: "https://my-server/upload" }}>
            <LogProgress />
            <UploadButton />
          </Uploady>
        </S.UploadSection>
      </S.Content>
    </S.AppContainer>
  );
}

export default App;
