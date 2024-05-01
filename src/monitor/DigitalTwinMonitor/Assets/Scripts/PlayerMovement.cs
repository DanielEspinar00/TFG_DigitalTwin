using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public Transform GameCamera;
    public float playerSpeed = 6.0f;
    public float turnSmoothTime = 0.1f;
    public float JumpForce = 1.0f;

    private CharacterController m_Controller;   // Set min movement to 0 so groundcheck works properly
    private Vector3 playerVelocity;
    private bool groundedPlayer;
    public float gravityValue = -9.81f;
    private float turnSmoothVelocity;

    private void Start()
    {
        Cursor.lockState = CursorLockMode.Locked;
        m_Controller = gameObject.GetComponent<CharacterController>();
    }

    void Update()
    {
        groundedPlayer = m_Controller.isGrounded;

        if (groundedPlayer && playerVelocity.y < 0)
        {
            playerVelocity.y = 0f;
        }

        Vector3 direction = new Vector3(Input.GetAxisRaw("Horizontal"), 0f, Input.GetAxisRaw("Vertical")).normalized;

        if (direction.magnitude >= 0.1f)    // There is input to move
        {
            float targetAngle = Mathf.Atan2(direction.x, direction.z) * Mathf.Rad2Deg + GameCamera.rotation.eulerAngles.y;  // Rotate player towards the move direction
            float angle = Mathf.SmoothDampAngle(transform.rotation.eulerAngles.y, targetAngle, ref turnSmoothVelocity, turnSmoothTime); // Make the rotation smooth
            transform.rotation = Quaternion.Euler(0f, angle, 0f);

            Vector3 moveDir = Quaternion.Euler(0f, angle, 0f) * Vector3.forward;    
            m_Controller.Move(moveDir.normalized * playerSpeed * Time.deltaTime);   // Move to the direction
        }

        Jump();

        playerVelocity.y += gravityValue * Time.deltaTime;  // Gravity force

        m_Controller.Move(playerVelocity * Time.deltaTime); // Aplly gravity force
    }

    private void Jump()
    {
        // Jump
        if (Input.GetButtonDown("Jump") && groundedPlayer)
        {
            playerVelocity.y = Mathf.Sqrt(JumpForce * -3.0f * gravityValue);
        }
    }
}
