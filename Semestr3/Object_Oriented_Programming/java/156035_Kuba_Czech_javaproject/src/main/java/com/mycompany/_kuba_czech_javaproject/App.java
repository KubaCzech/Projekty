/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany._kuba_czech_javaproject;

/**
 *
 * @author Kuba
 */
public class App {

    public static void main(String[] args) {
        Simulator simulation = new Simulator();
        java.awt.EventQueue.invokeLater(() -> {
            MyGUI gui = new MyGUI(simulation);
            gui.setVisible(true);
        });    }
}
