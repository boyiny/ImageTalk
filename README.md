# ImageTalk

This repository contains the code and example workflows for **ImageTalk** ([access paper by clicking this link](https://arxiv.org/abs/2512.09610)), a multimodal text-generation system designed to support people living with Motor Neuron Disease (plwMND) in augmentative and alternative communication (AAC) contexts.

ImageTalk was developed through both proxy-user-based and end-user-based iterative design phases, enabling efficient articulation of user needs and communication intent. The system achieves **95.6% keystroke savings**, maintains consistent performance, and received high user satisfaction ratings. It also contributes three design guidelines for AI-assisted text-generation systems and introduces four user-requirement levels tailored for AAC.

For full details, please refer to the accompanying paper.

---

## 🧪 Running ImageTalk 

Install dependencies:

### Step 1:
```bash
pip install -r requirements.txt
```

### Step 2:
Set your OpenAI API key before running in `story_generation.py`.

### Step 3: 
```bash
python app/app.py
```

### Step 4: 
Open your browser to the address Flask prints.

## 📚 Citation

If you use ImageTalk for research or development, please cite:
```bash
@article{yang2025imagetalk,
  title={ImageTalk: Multimodal Text Generation for AAC Support in Motor Neuron Disease},
  author={Yang, Boyin and Jiang, Puming and Kristensson, Per Ola},
  journal={arXiv preprint arXiv:2512.09610},
  year={2025}
}
```

## 📬 Contact

For questions or collaborations:
Boyin Yang – by266@cam.ac.uk

