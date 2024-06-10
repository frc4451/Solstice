{
  buildPythonPackage,
  fetchFromGitHub,
  hatchling,
  aiohttp,
  netifaces,
  numpy,
  opencv4,
  pythonRelaxDepsHook,
  lib,
}:
buildPythonPackage {
  pname = "mjpeg-streamer";
  version = "2024.2.8-unstable-2024-05-09";
  pyproject = true;

  # this is the on-demand branch (https://github.com/egeakman/mjpeg-streamer/pull/6)
  src = fetchFromGitHub {
    owner = "egeakman";
    repo = "mjpeg-streamer";
    rev = "4e63aaf4ec2d2967dd5ac57252e12392998e6cb9";
    hash = "sha256-DQMykaJAuOcE6T98DKmPsof7zgqs4pGNS/GfttYrKhw=";
  };

  buildInputs = [
    hatchling
  ];

  dependencies = [
    aiohttp
    netifaces
    numpy
    opencv4
  ];

  nativeBuildInputs = [pythonRelaxDepsHook];
  pythonRemoveDeps = ["opencv-python"]; # nix installs opencv as `opencv4`

  meta = {
    homepage = "https://pypi.org/project/mjpeg-streamer/";
    license = lib.licenses.agpl3Plus;
    # maintainers = with lib.maintainers; [archb1w];
    platforms = ["x86_64-linux"];
  };
}
