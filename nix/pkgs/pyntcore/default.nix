{
  buildPythonPackage,
  fetchPypi,
  lib,
  robotpy-wpiutil,
  robotpy-wpinet,
}:
buildPythonPackage rec {
  pname = "pyntcore";
  version = "2024.3.2.1";
  format = "wheel";

  src = fetchPypi {
    inherit pname version format;
    hash = "sha256-ElYglpo5nampCxgGyQqkZHbby4uaLwediI6wjajyBXw=";

    abi = "cp312";
    dist = "cp312";
    python = "cp312";
    platform = "manylinux_2_35_x86_64";
  };

  dependencies = [
    robotpy-wpinet
    robotpy-wpiutil
  ];

  meta = {
    homepage = "https://robotpy.github.io/";
    license = lib.licenses.bsd3;
    # maintainers = with lib.maintainers; [archb1w];
    platforms = ["x86_64-linux"];
  };
}
