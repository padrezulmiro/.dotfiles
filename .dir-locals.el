((python-mode
  . ((eval
      . (let* ((locals-dir (locate-dominating-file buffer-file-name
                                                   ".dir-locals.el"))
               (venv-path (concat locals-dir ".venv")))
          (azlcfg--activate-python-venv venv-path))))))
