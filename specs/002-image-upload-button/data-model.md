# Data Model: Image

This document describes the data model for the Image entity.

## Entity: Image

Represents an image file uploaded by the user.

### Fields

-   **file_name**: `string`
    -   The original name of the uploaded file.
-   **file_type**: `string`
    -   The MIME type of the file (e.g., `image/jpeg`, `image/png`).
-   **file_size**: `integer`
    -   The size of the file in bytes.
-   **content**: `bytes`
    -   The raw binary content of the image.

### Validation Rules

-   `file_type` must be one of `image/jpeg` or `image/png`.
-   `file_size` must be less than or equal to 10 MB.
