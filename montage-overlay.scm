(define (script-fu-montage-overlay
        input-folder
        overlay-image
        cell-width
        cell-height
        columns
        overlay-opacity)

  (let* (
        (filelist (cadr (file-glob (string-append input-folder "/*.jpg") 1)))
        (images '())
        (count (length filelist))
        (rows (ceiling (/ count columns)))
        (montage-width (* columns cell-width))
        (montage-height (* rows cell-height))
        (montage (car (gimp-image-new montage-width montage-height RGB)))
        (montage-layer (car (gimp-layer-new montage montage-width montage-height RGB-IMAGE "Montage" 100 NORMAL-MODE)))
        )

    ;; Add base layer
    (gimp-image-insert-layer montage montage-layer 0)

    ;; Load, resize, and paste each image
    (let loop ((lst filelist) (index 0))
      (if (null? lst)
          'done
          (let* (
                (filename (car lst))
                (img (car (gimp-file-load RUN-NONINTERACTIVE filename filename)))
                (layer (car (gimp-image-get-active-layer img)))
                (x (* (modulo index columns) cell-width))
                (y (* (quotient index columns) cell-height))
                )

            ;; Resize
            (gimp-image-scale img cell-width cell-height)

            ;; Copy/paste into montage
            (gimp-edit-copy layer)
            (let ((floating (car (gimp-edit-paste montage-layer FALSE))))
              (gimp-layer-set-offsets floating x y)
              (gimp-floating-sel-anchor floating)
            )

            ;; Clean up
            (gimp-image-delete img)

            ;; Next
            (loop (cdr lst) (+ index 1))
          )
      )
    )

    ;; Load overlay image
    (let* (
          (overlay-img (car (gimp-file-load RUN-NONINTERACTIVE overlay-image overlay-image)))
          (overlay-layer (car (gimp-image-get-active-layer overlay-img)))
          )

      ;; Scale overlay to montage size
      (gimp-image-scale overlay-img montage-width montage-height)

      ;; Copy overlay
      (gimp-edit-copy overlay-layer)
      (let ((floating (car (gimp-edit-paste montage-layer TRUE))))
        (gimp-layer-set-opacity floating overlay-opacity)
        (gimp-floating-sel-anchor floating)
      )

      ;; Clean up
      (gimp-image-delete overlay-img)
    )

    ;; Show final montage
    (gimp-display-new montage)
  )
)

(script-fu-register
 "script-fu-montage-overlay"
 "Montage + Overlay"
 "Creates a montage from a folder of images and overlays another image with adjustable opacity."
 "Mark’s Copilot"
 "Mark’s Copilot"
 "2026"
 ""
 SF-DIRNAME "Input Folder" ""
 SF-FILENAME "Overlay Image" ""
 SF-VALUE "Cell Width" "400"
 SF-VALUE "Cell Height" "600"
 SF-VALUE "Columns" "10"
 SF-VALUE "Overlay Opacity (0–100)" "50"
)

(script-fu-menu-register "script-fu-montage-overlay" "<Image>/Filters/Mark")
