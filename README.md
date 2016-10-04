# PsychoPy Implementation of Glasgow Face Matching Test

This repository contains a PsychoPy implementation of the Glasgow Face Matching Test by Burton, White, & McNeill (2010). It's been written using **PsychoPy 1.84.1**. If you find any issues with other versions, feel free to open an issue and/or pull request.

If you use this implementation, please cite it using the Zenodo DOI, as well as the original paper by Burton, A. M., White, D., & McNeill, A. (2010). *The Glasgow face matching test.* Behavior Research Methods, 42(1), 286-291.

## Setup

1. Download the stimuli from the [York FaceVar Lab](http://www.facevar.com/downloads/gfmt)
2. Put the **jpg stimuli** in a `stimuli` folder, with the short and long version in two separate folders. This is the expected directory tree

    ```
    └── stimuli
        ├── long
        │   ├── different
        │   │   ├── 003_020_L.jpg
        │   │   ├── ...
        │   └── same
        │       ├── 003_C2_DV.jpg
        │       ├── ...
        └── short
            ├── different
            │   ├── 013_235_R.jpg
            │   ├── ...  
            └── same
                ├── 020_C2_DV.jpg
                ├── ...
    ```

3. Use PsychoPy to run `gfmt.py`. Results will be under `./results`.

## Additional notes

Some minimal config can be changed in the `config.json` file, such as the parent stimulus directory, the results directory, and the response keys.