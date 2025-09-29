;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!

;; Doom exposes five (optional) variables for controlling fonts in Doom:
;;
;; - `doom-font' -- the primary font to use
;; - `doom-variable-pitch-font' -- a non-monospace font (where applicable)
;; - `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;; - `doom-unicode-font' -- for unicode glyphs
;; - `doom-serif-font' -- for the `fixed-pitch-serif' face

;; See 'C-h v doom-font' for documentation and more examples of what they
;; accept. For example:

;;(setq doom-font (font-spec :family "Fira Code" :size 12 :weight 'semi-light)
;;      doom-variable-pitch-font (font-spec :family "Fira Sans" :size 13))
;;
;; If you or Emacs can't find your font, use 'M-x describe-font' to look them
;; up, `M-x eval-region' to execute elisp code, and 'M-x doom/reload-font' to
;; refresh your font settings. If Emacs still can't find your font, it likely
;; wasn't installed correctly. Font issues are rarely Doom issues!

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:

;; (setq doom-theme 'doom-gruvbox)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
;; (setq org-directory "~/org/")

;; Whenever you reconfigure a package, make sure to wrap your config in an
;; `after!' block, otherwise Doom's defaults may override your settings. E.g.
;;
;;   (after! PACKAGE
;;     (setq x y))
;;
;; The exceptions to this rule:
;;
;;   - Setting file/directory variables (like `org-directory')
;;   - Setting variables which explicitly tell you to set them before their
;;     package is loaded (see 'C-h v VARIABLE' to look up their documentation).
;;   - Setting doom variables (which start with 'doom-' or '+').
;;
;; Here are some additional functions/macros that will help you configure Doom.
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;; Alternatively, use `C-h o' to look up a symbol (functions, variables, faces,
;; etc).
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.

;; Add load-paths for custom packages and modules
;; (load-path wasn't updated for a few modules)

(setq user-full-name "aZul"
      user-mail-address "fmdcosta.piano@gmail.com")

(setq doom-font (font-spec :family "Firacode Nerd Font Mono" :size 16))

(setq doom-everforest-background "soft")  ; or hard (defaults to soft)
(setq doom-everforest-light-background "soft") ; or hard (defaults to soft)
(setq doom-theme 'doom-everforest) ; dark variant

(defadvice! zcfg--set-doom-theme-after-consult-a (theme)
  "Sets `doom-theme' to theme regardless of `consult-theme' implementation.
currently, `doom-theme' isn't updated when selecting an already loaded
theme.

This fix is based on
https://github.com/doomemacs/doomemacs/issues/7511#issuecomment-1869710558"
  :after #'consult-theme
  (setq doom-theme theme))

(defgroup z-config nil
  "My own configuration"
  :group 'emacs)

(defcustom zcfg-day-theme 'doom-homage-white
  "Azul config's daytime theme"
  :group 'z-config)

(defcustom zcfg-night-theme 'doom-everforest
  "Azul config's nighttime theme"
  :group 'z-config)

(defcustom zcfg-contrast-theme 'doom-1337
  "Azul config's contrast theme"
  :group 'z-config)

(defcustom zcfg-sunrise-time "07:00am"
  "The time of sunrise"
  :type '(string)
  :group 'z-config)

(defcustom zcfg-sunset-time "06:00pm"
  "The time of sunset"
  :type '(string)
  :group 'z-config)

(defun zcfg--switch-day-night-themes (time)
  "Switch between day and night themes, e.g. after sunrise this function
updates the theme to `zcfg-day-theme' whether that's the current theme or
not. Likewise, for the night theme. TIME is one of two symbols `day' or
`night'"

  (cond ((eq time 'day)
         (unless (equal doom-theme zcfg-day-theme)
           (load-theme zcfg-day-theme :no-confirm)))
        ((eq time 'night)
         (unless (equal doom-theme zcfg-night-theme)
           (load-theme zcfg-night-theme :no-confirm)))))

(run-at-time zcfg-sunrise-time 86400 #'zcfg--switch-day-night-themes 'day)
(run-at-time zcfg-sunset-time 86400 #'zcfg--switch-day-night-themes 'night)

(setq display-line-numbers-type 'visual)

(global-display-fill-column-indicator-mode)

(map! :after org
      :map org-mode-map
      :localleader
      (:prefix ("B" . "org-babel")
       :desc "tangle" :nv "t" #'org-babel-tangle))

(setq org-directory "~/org/")

(setq evil-escape-key-sequence "fj")
(setq evil-escape-delay 0.20)

(add-hook 'find-file-hook 'recentf-save-list)

(setq which-key-allow-imprecise-window-fit nil)

(defun zcfg/activate-python-venv (venv-path)
  "Activate a python's virtual environment which was set up using its standard
library module venv.

The activation is achieved by checking if the given directory is named \".venv\""

  (let* ((venv-exists (file-exists-p venv-path)))
    (if venv-exists
      (progn
        (setq-local process-environment (copy-sequence
                                         process-environment))
        (setenv "path" (concat (expand-file-name venv-path)
                               "/bin:"
                               (getenv "path")))
        (setenv "pythonpath" (concat (expand-file-name venv-path) "/lib"))
        (setenv "virtual_env" venv-path)
        (setq-local lsp-pylsp-plugins-jedi-environment venv-path)
        (message "azul config: Activating python venv in %s" venv-path))
      (message "Didn't find a python venv directory!"))))

(defun zcfg/consult-imenu-toc ()
  "Select item from flattened and sorted `imenu' with preview.

The items are listed sorted according to their appearance in the buffer.

See also `consult-imenu'."
  (interactive)
  (consult-imenu--select
   "Go to item: "
   (consult--slow-operation "Building Imenu..."
     (zcfg--imenu-items-pos-sorted))))

(defun zcfg--imenu-items-pos-sorted ()
  "Return imenu items in order of buffer position.

If the items haven't been indexed yet, the indexation is executed."

;;; The cache may have not been built yet
  (unless (equal (car consult-imenu--cache) (buffer-modified-tick))
    (setq consult-imenu--cache
          (cons (buffer-modified-tick) (consult-imenu--compute))))
 
  (let* ((items (cdr consult-imenu--cache)))
    (seq-sort #'zcfg--imenu-item-less-than items)))

(defun zcfg--imenu-item-less-than (first-item second-item)
  ""
  (let* ((first-item-marker-pos (marker-position (cdr first-item)))
         (second-item-marker-pos (marker-position (cdr second-item))))
    (< first-item-marker-pos second-item-marker-pos)))
