# **InfinitiesSoft Toolbox**


## Usage

### Restriction
- `description` must be setting.
- `input` must be setting.
- `output` must be setting.
- `button` must be setting, and only one button.

### Sample
```
SSH:
  description: Generate SSH public and secret keys.
  input:
    KEY_LENGTH:
      name: key size (bits)
      type: combobox
      option:
        - 2048
        - 4096
    button:
      name: Generate
      type: button
      action: ssh-keygen -b $KEY_LENGTH -f id_rsa -N ''
  output:
    result:
      name: result
      type: textarea
      content:
        - id_rsa
        - id_rsa.pub
```

### Setting
- type
  - combobox
  - radio
  - text
  - password
  - textarea
  - button