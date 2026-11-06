/**
 * CareerPulse - Modern Interactive Web Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Auto dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      alert.style.opacity = "0";
      alert.style.transform = "translateY(-10px)";
      setTimeout(() => alert.remove(), 500);
    }, 5500);

    const closeBtn = alert.querySelector(".alert-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => alert.remove());
    }
  });

  // 2. Registration Page: Toggle Company Field based on role
  const roleRadios = document.querySelectorAll('input[name="role"]');
  const companyField = document.getElementById("companyFieldGroup");
  const companyInput = document.getElementById("company_name");

  if (roleRadios.length > 0 && companyField) {
    const updateRoleFields = () => {
      const selected = document.querySelector('input[name="role"]:checked')?.value;
      if (selected === "recruiter") {
        companyField.style.display = "block";
        if (companyInput) companyInput.required = true;
      } else {
        companyField.style.display = "none";
        if (companyInput) companyInput.required = false;
      }
    };
    roleRadios.forEach((r) => r.addEventListener("change", updateRoleFields));
    updateRoleFields();
  }

  // 3. Job Details Apply: Toggle Resume Source
  const resumeSourceRadios = document.querySelectorAll('input[name="resume_source"]');
  const customResumeWrap = document.getElementById("customResumeWrap");
  if (resumeSourceRadios.length > 0 && customResumeWrap) {
    const updateResumeSource = () => {
      const selected = document.querySelector('input[name="resume_source"]:checked')?.value;
      if (selected === "upload") {
        customResumeWrap.style.display = "block";
      } else {
        customResumeWrap.style.display = "none";
      }
    };
    resumeSourceRadios.forEach((r) => r.addEventListener("change", updateResumeSource));
    updateResumeSource();
  }

  // 4. Modal Helpers
  window.openModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.add("open");
      document.body.style.overflow = "hidden";
    }
  };

  window.closeModal = function (modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
      modal.classList.remove("open");
      document.body.style.overflow = "";
    }
  };

  // Close modal when clicking outside box
  document.querySelectorAll(".modal-backdrop").forEach((backdrop) => {
    backdrop.addEventListener("click", (e) => {
      if (e.target === backdrop) {
        backdrop.classList.remove("open");
        document.body.style.overflow = "";
      }
    });
  });

  // 5. Open Interview Scheduler Modal with Candidate Context
  window.openInterviewModal = function (appId, candidateName, jobTitle, existingDate, existingTime, existingMode, existingLink, existingNotes) {
    const modal = document.getElementById("interviewModal");
    if (!modal) return;

    const form = document.getElementById("interviewForm");
    if (form) {
      form.action = `/recruiter/applicant/${appId}/interview`;
    }

    const nameEl = document.getElementById("modalCandidateName");
    const jobEl = document.getElementById("modalJobTitle");
    if (nameEl) nameEl.textContent = candidateName;
    if (jobEl) jobEl.textContent = jobTitle;

    // Fill fields if previously set
    const dateInput = document.getElementById("interview_date");
    const timeInput = document.getElementById("interview_time");
    const modeInput = document.getElementById("interview_mode");
    const linkInput = document.getElementById("interview_link");
    const notesInput = document.getElementById("interview_notes");

    if (dateInput) dateInput.value = existingDate || "";
    if (timeInput) timeInput.value = existingTime || "";
    if (modeInput) modeInput.value = existingMode || "Google Meet";
    if (linkInput) linkInput.value = existingLink || "";
    if (notesInput) notesInput.value = existingNotes || "";

    openModal("interviewModal");
  };

  // 6. Open Candidate Details Modal
  window.openCandidateModal = function (candidate) {
    const modal = document.getElementById("candidateModal");
    if (!modal) return;

    document.getElementById("candName").textContent = candidate.name || "N/A";
    document.getElementById("candHeadline").textContent = candidate.headline || "Job Seeker";
    document.getElementById("candEmail").textContent = candidate.email || "N/A";
    document.getElementById("candPhone").textContent = candidate.phone || "N/A";
    document.getElementById("candSkills").textContent = candidate.skills || "Not specified";
    document.getElementById("candEducation").textContent = candidate.education || "Not specified";
    document.getElementById("candExperience").textContent = candidate.experience || "Not specified";
    document.getElementById("candBio").textContent = candidate.bio || "No summary provided.";

    const resumeLink = document.getElementById("candResumeLink");
    if (resumeLink) {
      if (candidate.resume) {
        resumeLink.href = `/resume/download/${candidate.resume}`;
        resumeLink.style.display = "inline-flex";
      } else {
        resumeLink.style.display = "none";
      }
    }

    openModal("candidateModal");
  };

  // 7. File Input label feedback
  document.querySelectorAll('input[type="file"]').forEach((fileInput) => {
    fileInput.addEventListener("change", function () {
      const fileName = this.files[0]?.name;
      const feedback = this.closest(".form-group")?.querySelector(".file-name-feedback");
      if (feedback && fileName) {
        feedback.textContent = `Selected: ${fileName}`;
        feedback.style.display = "block";
      }
    });
  });
});
