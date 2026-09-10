import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.overrideWebpackConfig((c) => c);
// 8 GB machine — keep the render lean.
Config.setConcurrency(2);
Config.setChromiumDisableWebSecurity(false);
