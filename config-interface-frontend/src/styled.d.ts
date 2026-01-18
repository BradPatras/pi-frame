import "styled-components";

declare module "styled-components" {
  export interface DefaultTheme {
    colors: {
      primary: string;
      secondary: string;
      background: string;
      cardBackground: string;
      text: string;
    };
    spacing: {
      small: string;
      medium: string;
      large: string;
      xlarge: string;
      xxlarge: string;
    };
    borderRadius: {
      small: string;
      medium: string;
    };
    breakpoints: {
      mobile: string;
    };
    fontSizes: {
      base: string;
      large: string;
    };
    shadows: {
      light: string;
      medium: string;
    };
  }
}
