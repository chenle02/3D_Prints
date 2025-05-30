# 3D Modeling Repository

A curated collection of personal 3D printing projects and gift designs.

Each project resides in its own folder and includes:
 - Source files (.3mf)
 - Printable exports (.stl, archives)
 - Documentation (README.md)
 
 ## Projects

 - **Tool Organizer (Goody Bag for Kailai's Birthday)**
   - **Path:** `202505_Tool_Organizer/`
   - **Description:** A custom-designed goody bag/tool organizer for Kailai's birthday.
   - **Original model:** [MakerWorld](https://makerworld.com/en/models/717173-tool-organizer#profileId-648086)
   - **License:** Standard Digital File License (SDFL)
   
 - **Heidi's Birthday Gift (Gridfinity Desk Organiser)**
   - **Path:** `202506_Birthday_Gift_Heidi/`
   - **Description:** Gridfinity desk organiser with custom words/logo for Heidi’s birthday.
   - **License:** Standard Digital File License (SDFL)

 - **Valentine Gifts (Custom Phone Stands)**
   - **Path:** `202502_Valentine_gifts/`
   - **Description:** Personalized phone stands as Valentine’s gifts.

 - **Zhihe Gift (Custom Gift Box for Zhihe Wu’s 6th Birthday)**
   - **Path:** `202502_Zhihe_Gift/`
   - **Description:** Custom gift box for Zhihe Wu’s 6th birthday.
   - **License:** Standard Digital File License (SDFL)

 ## Getting Started

 1. **Clone the repository**  
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

 2. **Install dependencies**  
    ```bash
    pip3 install -r requirements.txt
    ```

 3. **(Optional) Enable Git hooks**  
    ```bash
    scripts/install_hooks.sh
    ```

 4. **Browse projects**  
    Explore each project folder for source files, exports, and documentation.

 5. **Preview & print**  
    - Open `.3mf` files with PrusaSlicer or another 3MF-compatible slicer.  
    - Slice and print the `.stl` files on your preferred 3D printer.

## Contributing

We welcome contributions! To add a new project:

1. Create a folder named `YYYYMM_ProjectName`.
2. Add source files (.3mf) and export files (.stl, archives).
3. Include a `README.md` with project details and printing instructions.
4. Update this top-level `README.md` under **Projects**.

For detailed guidelines, see `.codex/Instructions.md`.

